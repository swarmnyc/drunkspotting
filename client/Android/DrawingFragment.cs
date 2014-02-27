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
using Android.Graphics.Drawables;

namespace DrunkSpotting
{
	public class DrawingFragment : Android.Support.V4.App.Fragment
	{
		//        protected override void OnCreate(Bundle bundle)
		//        {
		//            base.OnCreate(bundle);
		//
		//            // Create your application here
		//        }

		Bitmap bmp;
		DrawingCanvasView mDrawingView;

		public override View OnCreateView( LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState )
		{
			base.OnCreateView( inflater, container, savedInstanceState );
			 mDrawingView = new DrawingCanvasView( Activity );
			bmp = (Bitmap) Arguments.GetParcelable( "image" ) ;

			mDrawingView.Image = bmp ;
			return mDrawingView;
		}

		public override void OnViewCreated( View view, Bundle savedInstanceState )
		{
			base.OnViewCreated( view, savedInstanceState );



		}

	}
}

