
using System;
using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Util;
using Android.Views;
using Android.Widget;
using Android.Graphics;
using Android.Views.Animations;
using Android.Graphics.Drawables;
using System.Net;
using DrunkSpotting;
using System.Threading.Tasks;
using System.Threading;

namespace DrunkSpotting
{
    public class FadeImageView : ImageView
    {
        Animation fadeInAnimation;
        Animation fadeOutAnimation;

        public event EventHandler DownloadingImage ;
        public event EventHandler DownloadedImage;

        private static BitmapCache _cache;

        BitmapCache Cache
        {
            get
            {
                return _cache ?? (_cache = BitmapCache.CreateCache(this.Context, "DrunkSpotting"));
            }
        }

        CancellationTokenSource tokenSource2;
        CancellationToken ct ;
        Task currentTask = null;
        Bitmap currrentBitmap;
        object bitmapLock = new object();
        ImageService _imageService = null;
        private const string TAG = "FadeImageView";

        public FadeImageView(Context ctx) : base (ctx)
        {
            Initialize();
        }

        public FadeImageView(Context context, IAttributeSet attrs) :
            base (context, attrs)
        {
            Initialize();
        }

        public FadeImageView(Context context, IAttributeSet attrs, int defStyle) :
            base (context, attrs, defStyle)
        {
            Initialize();
        }

        void Initialize()
        {
            tokenSource2 = new CancellationTokenSource();
            ct = tokenSource2.Token;

            _imageService = new ImageService(this.Context);

            fadeInAnimation = new AlphaAnimation(0, 1) {
                Duration = 500
            };
            fadeOutAnimation = new AlphaAnimation(1, 0) {
                Duration = 100
            };
        }

        void DoAnimation(bool really, Action changePic)
        {
            if (!really)
                changePic();
            else
            {
                EventHandler<Animation.AnimationEndEventArgs> callback = (s, e) => {
                    changePic();
                    StartAnimation(fadeInAnimation);
                    fadeOutAnimation.AnimationEnd -= callback;
                };
                fadeOutAnimation.AnimationEnd += callback;
                StartAnimation(fadeOutAnimation);
            }
        }

        public void SetImageBitmap(Bitmap bm, bool animate)
        {
            DoAnimation(animate, () => SetImageBitmap(bm));
        }

        public void SetImageDrawable(Drawable drawable, bool animate)
        {
            DoAnimation(animate, () => SetImageDrawable(drawable));
        }

        public void SetImageResource(int resId, bool animate)
        {
            DoAnimation(animate, () => SetImageResource(resId));
        }

        public void SetImageURI(Android.Net.Uri uri, bool animate)
        {
            DoAnimation(animate, () => SetImageURI(uri));
        }

        public void CleanUp()
        {
//                if (null != currentTask)
//                {
//                    tokenSource2.Cancel();
//                }
//          
//          lock (bitmapLock)
//          {
            if (null != currrentBitmap && ! currrentBitmap.IsRecycled)
            {
            currrentBitmap.Recycle();
            }
            SetImageBitmap(null, false);
//                if (null != currrentBitmap)
//                {
//                    Log.Info("*****", "Recycling image");
//                    currrentBitmap.Recycle();
//                }
//                currrentBitmap = null;
//            }

        }

//       
//        protected override void OnMeasure(int widthMeasureSpec, int heightMeasureSpec)
//        {
//            Drawable drawable = this.Drawable;
//            if (drawable != null)
//            {
//                int width =  MeasureSpec.GetSize(widthMeasureSpec);
//                int diw = drawable.IntrinsicWidth;
//                if (diw > 0)
//                {
//                    int height = width * drawable.IntrinsicHeight / diw;
//                    SetMeasuredDimension(width, height);
//                }
//                else
//                    base.OnMeasure(widthMeasureSpec, heightMeasureSpec);
//            }
//            else
//                base.OnMeasure(widthMeasureSpec, heightMeasureSpec);
//        }
//    

        void OnImageUrlChange()
        {
            Bitmap cachedImage = null;
            if (Cache.TryGet(ImageUrl, out cachedImage))
            {
                if (!cachedImage.IsRecycled)
                {
                    Log.Info(TAG, "*** Cache hit for Url" + ImageUrl);
                    currrentBitmap = cachedImage;
                    SetImageBitmap(cachedImage, true);
                    return;
                }
            }

          

            var task = Task.Factory.StartNew(() =>
            {
                // Were we already canceled?
                ct.ThrowIfCancellationRequested();

                if (null != DownloadingImage)
                {
                    DownloadingImage(this, null);
                }

                _imageService.DownloadImage(ImageUrl, (b, url) => {
                    Log.Info(TAG, "Url = {2}\nSize = {0},{1}", b.Width, b.Height, url);
                    var croppedBitmap = CropToScreenWidth(b);
                    Cache.AddOrUpdate(url, croppedBitmap, TimeSpan.FromDays(7));

                    ((Activity)Context).RunOnUiThread(() => {
                        
                        if (ct.IsCancellationRequested)
                        {
                            // Clean up here, then...
                            ct.ThrowIfCancellationRequested();
                        } else
                        {

                            lock (bitmapLock)
                            {
                                currrentBitmap = croppedBitmap;
                            }
                            if (ImageUrl == url)
                            {

                                SetImageBitmap(croppedBitmap, true);
                                if (null != DownloadedImage)
                                {
                                    DownloadedImage(this, null);
                                }
                            }
                           
                        }
                    });
                }, (e, url) => {
                    Log.Error(TAG, e.ToString());
                });
            });


        }

        private Bitmap CropToScreenWidth(Bitmap b)
        {
            var tmp = ((Activity)Context).WindowManager;
            IWindowManager windowManager = tmp;
            DisplayMetrics displayMetrics = new DisplayMetrics();
            windowManager.DefaultDisplay.GetMetrics(displayMetrics);


//            int maxWidth = displayMetrics.WidthPixels;
            int maxWidth = this.MeasuredWidth;



            int originalWidth = b.Width;
            int originalHeight = b.Height;

            if (originalWidth > 0)
            {
                float scale = 0f; 
                int croppedWidth = 0;

                if (originalWidth >= originalHeight)
                {
                    int offset = (originalWidth - originalHeight);
                    croppedWidth = (originalWidth - offset);
                    scale = (float)maxWidth / (float)croppedWidth;
                } else
                {
                    int offset = (originalHeight - originalWidth);
                    croppedWidth = originalWidth;
                    scale = (float)maxWidth / (float)croppedWidth;
                }

                int length = (int)(croppedWidth * scale);

                Log.Debug(TAG, String.Format("Scaling image by {0} to ({1})", scale, length));
                    
                Matrix matrix = new Matrix();
                matrix.PostScale(scale, scale);

                int x = (int)((b.Width * scale - length) / scale) / 2;
                int y = (int)((b.Height * scale - length) / scale) / 2;

                x = Math.Max(0, x);
                y = Math.Max(0, y);

                Log.Debug(TAG, String.Format("Cropping Image {0}, {1}", x, y));
                return Bitmap.CreateBitmap(b, x, y, croppedWidth, croppedWidth, matrix, true);
               
            }

            return b;
        }

        private string _imageUrl = null;

        public String ImageUrl
        {
            get
            {
                return _imageUrl;
            }
            set
            {
                if (_imageUrl != value)
                {
                    _imageUrl = value;

                    OnImageUrlChange();
                }               
            }
        }
    }
}

