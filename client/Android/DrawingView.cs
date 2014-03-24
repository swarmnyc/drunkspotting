using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Util;
using Android.Views;
using Android.Widget;
using Android.Graphics;

namespace DrunkSpotting
{
	public class DrawingView : View, View.IOnTouchListener
	{
		private static readonly float STROKE_WIDTH = 5f;
		/** Need to track this so the dirty region can accommodate the stroke. **/
		private static readonly float HALF_STROKE_WIDTH = STROKE_WIDTH / 2;
		private Paint paint = new Paint();
		private Path path = new Path();
		/**
       * Optimizes painting by invalidating the smallest possible area.
       */
		private float lastTouchX;
		private float lastTouchY;
		private readonly RectF dirtyRect = new RectF();

		Canvas _canvas;

		Bitmap _bitmap;
		bool _isBitmapShownOnCanvas = false;

		public  bool OnTouch( View v, MotionEvent ev )
		{
			// Log.d("jabagator", "onTouch: " + event);
			float eventX = ev.GetX();
			float eventY = ev.GetY();

			switch (ev.Action)
			{
			case MotionEventActions.Down:
				path.MoveTo( eventX, eventY );
				lastTouchX = eventX;
				lastTouchY = eventY;
					// No end point yet, so don't waste cycles invalidating.
				return true;

			case MotionEventActions.Move:
			case MotionEventActions.Up:
					// Start tracking the dirty region.
				resetDirtyRect( eventX, eventY );

					// When the hardware tracks events faster than 
					// they can be delivered to the app, the
					// event will contain a history of those skipped points.
				int historySize = ev.HistorySize;
				for( int i = 0; i < historySize; i++ )
				{
					float historicalX = ev.GetHistoricalX( i );
					float historicalY = ev.GetHistoricalY( i );
					expandDirtyRect( historicalX, historicalY );
					path.LineTo( historicalX, historicalY );
				}

					// After replaying history, connect the line to the touch point.
				path.LineTo( eventX, eventY );
				break;

			default:
//					Log.d("jabagator", "Unknown touch event  " + event.toString());
				return false;
			}

			// Include half the stroke width to avoid clipping.
			Invalidate(
				(int) ( dirtyRect.Left - HALF_STROKE_WIDTH ),
				(int) ( dirtyRect.Top - HALF_STROKE_WIDTH ),
				(int) ( dirtyRect.Right + HALF_STROKE_WIDTH ),
				(int) ( dirtyRect.Bottom + HALF_STROKE_WIDTH ) );

			lastTouchX = eventX;
			lastTouchY = eventY;

			return true;
		}

		/**
           * Called when replaying history to ensure the dirty region 
           * includes all points.
           */
		private void expandDirtyRect( float historicalX, float historicalY )
		{
			if ( historicalX < dirtyRect.Left )
			{
				dirtyRect.Left = historicalX;
			} else if ( historicalX > dirtyRect.Right )
			{
				dirtyRect.Right = historicalX;
			}
			if ( historicalY < dirtyRect.Top )
			{
				dirtyRect.Top = historicalY;
			} else if ( historicalY > dirtyRect.Bottom )
			{
				dirtyRect.Bottom = historicalY;
			}
		}

		/**
           * Resets the dirty region when the motion event occurs.
           */
		private void resetDirtyRect( float eventX, float eventY )
		{

			// The lastTouchX and lastTouchY were set when the ACTION_DOWN
			// motion event occurred.
			dirtyRect.Left = Math.Min( lastTouchX, eventX );
			dirtyRect.Right = Math.Max( lastTouchX, eventX );
			dirtyRect.Top = Math.Min( lastTouchY, eventY );
			dirtyRect.Bottom = Math.Max( lastTouchY, eventY );
		}

		/** DrawingView readonlyructor */

		public DrawingView( Context context ) :
			base( context )
		{
			Initialize();
		}

		public DrawingView( Context context, IAttributeSet attrs ) :
			base( context, attrs )
		{
			Initialize();
		}

		public DrawingView( Context context, IAttributeSet attrs, int defStyle ) :
			base( context, attrs, defStyle )
		{
			Initialize();
		}

		void Initialize()
		{
			paint.AntiAlias = ( true );
			paint.Color = ( Color.Blue );
			paint.SetStyle( Paint.Style.Stroke );
			paint.StrokeJoin = ( Paint.Join.Round );
			paint.StrokeWidth = ( STROKE_WIDTH );

			SetOnTouchListener(this);

		}

		public void SetBitmap(Bitmap b)
		{
			_bitmap = b;
		}


		public void clear()
		{
			path.Reset();

			// Repaints the entire view.
			Invalidate();
		}

		protected override void OnDraw( Canvas canvas )
		{
			_canvas = canvas;
			if (null != _bitmap )
			{
				canvas.DrawBitmap(_bitmap, new Matrix(), new Paint() );
			}
			canvas.DrawPath( path, paint );
		}
	}
}

