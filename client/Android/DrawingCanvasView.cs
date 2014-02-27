using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using Mono.Security.X509;
using Android.Graphics;
using System.Runtime.CompilerServices;

namespace DrunkSpotting
{
	public class DrawingCanvasView : View , Android.Views.View.IOnTouchListener
	{
		public Bitmap Image { get; set; }

		Path mPath;

		List<Path> paths = new List<Path>();

		Paint mPaint;

		Canvas mCanvas;

		float mX;
		float mY;
		private static readonly float TOUCH_TOLERANCE = 4;

		public DrawingCanvasView( Context context ) : base( context )
		{

			Init();
		}
		

		public DrawingCanvasView( Context context, Android.Util.IAttributeSet attrs ) : base( context, attrs )
		{
			Init();

		}

	
		
		void Init()
		{
			Focusable = (true);
			FocusableInTouchMode = (true);

			this.SetOnTouchListener(this);

			mPaint = new Paint();
			mPaint.AntiAlias = (true);
			mPaint.Dither = (true);
			mPaint.Color = Color.Black;
			mPaint.SetStyle (Paint.Style.Stroke);
			mPaint.StrokeJoin = (Paint.Join.Round);
			mPaint.StrokeCap = (Paint.Cap.Round);
			mPaint.StrokeWidth = (6);
			mCanvas = new Canvas();
			mPath = new Path();
			paths.Add(mPath);
		}

		protected override void OnDraw(Android.Graphics.Canvas canvas)
		{
			canvas.DrawBitmap(Image, new Matrix(), mPaint);


			foreach (Path p in paths){
				canvas.DrawPath(p, mPaint);
			}
		}

		public bool OnTouch( View v, MotionEvent e )
		{
			float x = e.GetX();
			float y = e.GetY();

			switch (e.Action) {
			case MotionEventActions.Down:
				touch_start(x, y);
				Invalidate();
				break;
			case MotionEventActions.Move:
				touch_move(x, y);
				Invalidate();
				break;
			case MotionEventActions.Up:
				touch_up();
				Invalidate();
				break;
			}
			return true;
		}

//		public override bool OnTouchEvent(MotionEvent e)
//		{
//			return base.OnTouchEvent(e);
//		}

		private void touch_start(float x, float y) {
			mPath.Reset();
			mPath.MoveTo(x, y);
			mX = x;
			mY = y;
		}
		private void touch_move(float x, float y) {
			float dx = Math.Abs(x - mX);
			float dy = Math.Abs(y - mY);
			if (dx >= TOUCH_TOLERANCE || dy >= TOUCH_TOLERANCE) {
				mPath.QuadTo(mX, mY, (x + mX)/2, (y + mY)/2);
				mX = x;
				mY = y;
			}
		}
		private void touch_up() {
			mPath.LineTo(mX, mY);
			// commit the path to our offscreen
			mCanvas.DrawPath(mPath, mPaint);
			// kill this so we don't double draw            
			mPath = new Path();
			paths.Add(mPath);
		}

	}
}

