using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using Android.Graphics;
using Android.Provider;
using Java.IO;
using Android.Util;
using Android.Net;
using Android;

namespace DrunkSpotting
{
	public class DrawOnPhotoFragment : Android.Support.V4.App.Fragment, View.IOnTouchListener
	{

		ImageView _imageView;
		Button savePicture;
		Bitmap bmp;
		Bitmap alteredBitmap;
		Canvas canvas;
		Matrix matrix;
		float downx = 0;
		float downy = 0;
		float upx = 0;
		float upy = 0;

		private static  float STROKE_WIDTH = 20f;

		/** Need to track this so the dirty region can accommodate the stroke. **/
		private static  float HALF_STROKE_WIDTH = STROKE_WIDTH / 2;

		private Paint paint = new Paint();
		private Android.Graphics.Path path = new Android.Graphics.Path();
		private float lastTouchX;
		private float lastTouchY;
		private RectF dirtyRect = new RectF();


		public static DrawOnPhotoFragment GetInstance(Bitmap b)
		{
			var fragment = new DrawOnPhotoFragment();
			Bundle bundle = new Bundle();
			bundle.PutParcelable("image", b);
			fragment.Arguments = bundle;

			return fragment;
		}

		public override View OnCreateView( LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState )
		{
			_imageView = new ImageView( Activity );
			return _imageView;
		}

		public override void OnViewCreated( View view, Bundle savedInstanceState )
		{
			base.OnViewCreated( view, savedInstanceState );


			bmp = (Bitmap) Arguments.GetParcelable( "image" );

			alteredBitmap = Bitmap.CreateBitmap( bmp.Width, bmp
				.Height, bmp.GetConfig() );

			canvas = new Canvas( alteredBitmap );
			paint = new Paint();
//			paint.Color = ( Color.Aqua );
//			paint.StrokeWidth = 10;
			paint.AntiAlias = true;// (true);
			paint.Color= Color.Wheat;
			paint.SetStyle(Paint.Style.Stroke);
			paint.StrokeJoin = Paint.Join.Round;
			paint.StrokeWidth = STROKE_WIDTH;
			matrix = new Matrix();
			canvas.DrawBitmap( bmp, matrix, paint );

//			paint.setAntiAlias(true);
//			paint.setColor(Color.WHITE);
//			paint.setStyle(Paint.Style.STROKE);
//			paint.setStrokeJoin(Paint.Join.ROUND);
//			paint.setStrokeWidth(STROKE_WIDTH);

			_imageView.SetImageBitmap( alteredBitmap );
			_imageView.SetOnTouchListener( this );


		}

//		public bool OnTouch( View v, MotionEvent ev )
//		{
//			MotionEventActions action = ev.Action;
//			switch (action)
//			{
//			case MotionEventActions.Down:
//
//				downx = ev.GetX();
//				downy = ev.GetY();
//				Log.Debug( Class.SimpleName, string.Format( "Down [{0},{1}]", downx, downy ) );
//				break;
//			case MotionEventActions.Move:
//				Android.Graphics.Path path = new Android.Graphics.Path();
//				path.MoveTo( downx, downy );
//				for( int i = 0; i < ev.HistorySize; i++ )
//				{
//					Log.Debug( Class.SimpleName, string.Format( "{0}: [{1},{2}]", i, ev.GetHistoricalX( i ), ev.GetHistoricalY( i ) ) );
//					path.LineTo( ev.GetHistoricalX( i ), ev.GetHistoricalY( i ) );
//				}
//				downx = ev.GetX();
//				downy = ev.GetY();
//				Log.Debug( Class.SimpleName, string.Format( "Move [{0},{1}]", downx, downy ) );
//				path.LineTo( downx, downy );
//				canvas.DrawPath( path, paint );
//				_imageView.Invalidate();
//				break;
//			case MotionEventActions.Up:
//				upx = ev.GetX();
//				upy = ev.GetY();
//				canvas.DrawLine( downx, downy, upx, upy, paint );
//				_imageView.Invalidate();
//				break;
//			case MotionEventActions.Cancel:
//				break;
//			default:
//				break;
//			}
//			return true;
//		}

		public bool OnTouch(View v, MotionEvent ev) {
			// Log.d("jabagator", "onTouch: " + event);
			float eventX = ev.GetX();
			float eventY = ev.GetY();

			switch (ev.Action) 
			{
			case MotionEventActions.Down:
				path.MoveTo(eventX, eventY);
				lastTouchX = eventX;
				lastTouchY = eventY;
				// No end point yet, so don't waste cycles invalidating.
				return true;

			case MotionEventActions.Move:
			case MotionEventActions.Up:
				// Start tracking the dirty region.
				resetDirtyRect(eventX, eventY);

				// When the hardware tracks events faster than 
				// they can be delivered to the app, the
				// event will contain a history of those skipped points.
				int historySize = ev.HistorySize;
				for (int i = 0; i < historySize; i++) {
					float historicalX = ev.GetHistoricalX(i);
					float historicalY = ev.GetHistoricalY(i);
					expandDirtyRect(historicalX, historicalY);
					path.LineTo(historicalX, historicalY);
				}

				// After replaying history, connect the line to the touch point.
				path.LineTo(eventX, eventY);
				break;

			default:
//				Log.d("jabagator", "Unknown touch event  " + ev.toString());
				return false;
			}

			// Include half the stroke width to avoid clipping.
			_imageView.Invalidate(
				(int) (dirtyRect.Left - HALF_STROKE_WIDTH),
				(int) (dirtyRect.Top - HALF_STROKE_WIDTH),
				(int) (dirtyRect.Right + HALF_STROKE_WIDTH),
				(int) (dirtyRect.Bottom + HALF_STROKE_WIDTH));

			canvas.DrawPath( path, paint );

			lastTouchX = eventX;
			lastTouchY = eventY;

			return true;
		}



		/**
           * Called when replaying history to ensure the dirty region 
           * includes all points.
           */
		private void expandDirtyRect(float historicalX, float historicalY) {
			if (historicalX < dirtyRect.Left) {
				dirtyRect.Left = historicalX;
			} else if (historicalX > dirtyRect.Right) {
				dirtyRect.Right = historicalX;
			}
			if (historicalY < dirtyRect.Top) {
				dirtyRect.Top = historicalY;
			} else if (historicalY > dirtyRect.Bottom) {
				dirtyRect.Bottom = historicalY;
			}
		}

		/**
           * Resets the dirty region when the motion event occurs.
           */
		private void resetDirtyRect(float eventX, float eventY) {

			// The lastTouchX and lastTouchY were set when the ACTION_DOWN
			// motion event occurred.
			dirtyRect.Left = Math.Min(lastTouchX, eventX);
			dirtyRect.Right = Math.Max(lastTouchX, eventX);
			dirtyRect.Top = Math.Min(lastTouchY, eventY);
			dirtyRect.Bottom = Math.Max(lastTouchY, eventY);
		}

//		public void OnClick( View v )
//		{
//			if ( alteredBitmap != null )
//			{
//				ContentValues contentValues = new ContentValues( 3 );
//				contentValues.Put( Android.Provider.MediaStore.Images.Media.InterfaceConsts.DisplayName, "Draw On Me" );
//                    
////				Android.Net.Uri imageFileUri = ContentResolver.Insert( Android.Provider.MediaStore.Images.Media.ExternalContentUri,
////					                               contentValues );
//				try
//				{
////					Stream imageFileOS = ContentResolver.OpenOutputStream( imageFileUri );
////					alteredBitmap.Compress( Bitmap.CompressFormat.Jpeg, 90, imageFileOS );
//					Toast t = Toast.MakeText( Activity, "Saved!", ToastLength.Short );
//					t.Show();
//                        
//				} catch ( Exception e )
//				{
//					Log.Error( "EXCEPTION", e.Message );
//				}
//			}
//
//		}
	}
}

