using System;
using Android.Content;
using Android.Util;
using Android.Graphics;
using Java.Net;
using Android.Views;
using Android.App;
using System.Threading;

namespace DrunkSpotting
{
	public class ImageService
	{
		public Context Context { get; set; }

		public ImageService (Context context)
		{
			this.Context = context;
		}

		void DownloadImage2 (string url, Action<Bitmap> onComplete, Action<Exception> onError)
		{
			Bitmap bitmap = null;
			//Decode image size
			BitmapFactory.Options o = new BitmapFactory.Options ();
			o.InJustDecodeBounds = true;
			//			final CelebrityTrackerApplication celebrityTrackerApplication = CelebrityTrackerApplication.getInstance();
			try {
				BitmapFactory.DecodeStream ((new URL (url).OpenStream ()), null, o);
			}
			catch (Exception e) {
				Log.Error ("ViewHelper.ViewHelper.setImageFromMedia", String.Format ("Failed to load image from url: {0}", url), e);
				onError (e);
			}
			var tmp = ((Activity)Context).WindowManager;
			IWindowManager windowManager = tmp;
			//	(IWindowManager)Context.GetSystemService (Context.WindowService);
			DisplayMetrics displayMetrics = new DisplayMetrics ();
			windowManager.DefaultDisplay.GetMetrics (displayMetrics);
			int maxSize = Math.Max (displayMetrics.WidthPixels, displayMetrics.HeightPixels);
			int scale = 1;

			if (o.OutHeight > maxSize || o.OutWidth > maxSize) {
				scale = (int)Math.Pow (2, (int)Math.Round (Math.Log (maxSize / (double)Math.Max (o.OutHeight, o.OutWidth)) / Math.Log (0.5)));
			}
			Log.Info ("Image Service", "### ImageSize = ({0},{1}), ScreenSize = ({2},{3}) Calculated scale = {4}", 
			          o.OutWidth, o.OutHeight,
			          displayMetrics.WidthPixels, displayMetrics.HeightPixels,
			          scale);
			BitmapFactory.Options o2 = new BitmapFactory.Options ();
			//if (shouldScale)
			//{
			o2.InSampleSize = scale;
			//}
			o2.InDither = true;
			//            o2.InScaled = true;
			//            o2.InDensity = 4;
			//            o2.InTargetDensity = 2;
			o2.InPurgeable = true;
			//o2.inInputShareable = true;
			try {
				bitmap = BitmapFactory.DecodeStream ((new URL (url).OpenStream ()), null, o2);
			}
			catch (Exception e) {
				Log.Error ("ViewHelper.ViewHelper.setImageFromMedia", String.Format ("Failed to load image from url: {0}", url), e);
			}
			if (null != bitmap) {
				Log.Debug ("BitmapPerformanceTest", String.Format ("Bitmap dimensions {0}, {1}, Density = {2}", bitmap.Width, bitmap.Height, bitmap.Density));
				//				aImageView.setImageBitmap( bitmap );
				onComplete (bitmap);
			}
			else {
				onError (new ApplicationException ("Failed to load Bitmap from Url: " + url));
			}
		}

		public void DownloadImage (string url, Action<Bitmap> onComplete, Action<Exception> onError)
		{

			ThreadPool.QueueUserWorkItem( (x) => DownloadImage2 (url, onComplete, onError) );

		}

	}
}

