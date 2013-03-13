
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

namespace DrunkSpotting
{
	public class FadeImageView : ImageView
	{
		Animation fadeInAnimation;
		Animation fadeOutAnimation;

		public event EventHandler DownloadingImage ;
		public event EventHandler DownloadedImage;

		Bitmap currrentBitmap;
		object bitmapLock = new object ();
		ImageService _imageService = null;
		private const string TAG = "FadeImageView";

		public FadeImageView (Context ctx) : base (ctx)
		{
			Initialize ();
		}

		public FadeImageView (Context context, IAttributeSet attrs) :
			base (context, attrs)
		{
			Initialize ();
		}

		public FadeImageView (Context context, IAttributeSet attrs, int defStyle) :
			base (context, attrs, defStyle)
		{
			Initialize ();
		}

		void Initialize ()
		{
			_imageService = new ImageService (this.Context);

			fadeInAnimation = new AlphaAnimation (0, 1) {
				Duration = 500
			};
			fadeOutAnimation = new AlphaAnimation (1, 0) {
				Duration = 100
			};
		}

		void DoAnimation (bool really, Action changePic)
		{
			if (!really)
				changePic ();
			else {
				EventHandler<Animation.AnimationEndEventArgs> callback = (s, e) => {
					changePic ();
					StartAnimation (fadeInAnimation);
					fadeOutAnimation.AnimationEnd -= callback;
				};
				fadeOutAnimation.AnimationEnd += callback;
				StartAnimation (fadeOutAnimation);
			}
		}

		public void SetImageBitmap (Bitmap bm, bool animate)
		{
			DoAnimation (animate, () => SetImageBitmap (bm));
		}

		public void SetImageDrawable (Drawable drawable, bool animate)
		{
			DoAnimation (animate, () => SetImageDrawable (drawable));
		}

		public void SetImageResource (int resId, bool animate)
		{
			DoAnimation (animate, () => SetImageResource (resId));
		}

		public void SetImageURI (Android.Net.Uri uri, bool animate)
		{
			DoAnimation (animate, () => SetImageURI (uri));
		}

		public void DownloadImage ()
		{

			if (null != DownloadingImage) {
				DownloadingImage (this, null);
			}
			SetImageBitmap (null);
			// Downlaod Image Bitmap
			var webClient = new WebClient ();

			webClient.DownloadDataCompleted += (s, e) => {
				var bytes = e.Result; // get the downloaded data
//				string documentsPath = Environment.GetFolderPath(Environment.SpecialFolder.Personal);
//				string localFilename = "downloaded.png";
//				string localPath = Path.Combine (documentsPath, localFilename);
//				File.WriteAllBytes (localpath, bytes); // writes to local storage

				// Set bitmap
				if (null == bytes || bytes.Length == 0) {
					DownloadedImage (this, null);
					return;
				}
				var bitmap = BitmapFactory.DecodeByteArray (bytes, 0, bytes.Length);
				((Activity)Context).RunOnUiThread (() => 
				{
					// Clear image
					if (null != currrentBitmap) {
						lock (bitmapLock) {
							if (null != currrentBitmap) {
								Log.Info ("*****", "Recycling image");
								currrentBitmap.Recycle ();

							}
						}
					}
					lock (bitmapLock) {
						currrentBitmap = bitmap;
					}

					if (null != DownloadedImage) {
						DownloadedImage (this, null);
					}

					SetImageBitmap (bitmap, true);
				});
			};

			webClient.DownloadDataAsync (new Uri (ImageUrl), ImageUrl);

		}

		private string _imageUrl = null;

		public String ImageUrl {
			get {
				return _imageUrl;
			}
			set {
				if (_imageUrl != value) {
					_imageUrl = value;
					if (null != DownloadingImage) {
						DownloadingImage (this, null);
					}
					SetImageBitmap (null);
					_imageService.DownloadImage (ImageUrl, b => {
						Log.Info (TAG, "Size = {0},{1}", b.Width, b.Height);
						var bitmap = b;
						((Activity)Context).RunOnUiThread (() => 
						{
							// Clear image
							if (null != currrentBitmap) {
								lock (bitmapLock) {
									if (null != currrentBitmap) {
										Log.Info ("*****", "Recycling image");
										currrentBitmap.Recycle ();
										currrentBitmap = null;
										
									}
								}
							}
							lock (bitmapLock) {
								currrentBitmap = bitmap;
							}
							
							if (null != DownloadedImage) {
								DownloadedImage (this, null);
							}
							
							SetImageBitmap (bitmap, true);
						});

					}, e => {
						Log.Error (TAG, e.ToString ());
					});
				}
			}
		}
	}
}

