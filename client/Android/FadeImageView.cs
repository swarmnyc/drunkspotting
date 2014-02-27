
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

		public Bitmap CurrrentBitmap
		{
			get
			{
				return currrentBitmap;
			}
			set
			{
				currrentBitmap = value;
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
//			lock (bitmapLock)
//			{
                SetImageBitmap(null, false);
//                if (null != currrentBitmap)
//                {
//                    Log.Info("*****", "Recycling image");
//                    currrentBitmap.Recycle();
//                }
//                currrentBitmap = null;
//            }

        }

       

        void OnImageUrlChange()
        {
            Bitmap cachedImage = null;
            if (Cache.TryGet(ImageUrl, out cachedImage))
            {
                
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

                    Cache.AddOrUpdate(url, b, TimeSpan.FromDays(7));

                    ((Activity)Context).RunOnUiThread(() => {
                        
						if (ct.IsCancellationRequested)
						{
							// Clean up here, then...
							ct.ThrowIfCancellationRequested();
						}
						else
						{

							lock (bitmapLock)
							{
								currrentBitmap = b;
							}
							if (ImageUrl == url)
							{
								SetImageBitmap(b);
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

