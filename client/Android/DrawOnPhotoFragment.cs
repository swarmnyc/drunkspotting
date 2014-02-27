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
	public class DrawOnPhotoFragment : Android.Support.V4.App.Fragment, View.IOnTouchListener, View.IOnClickListener
	{
		//        protected override void OnCreate(Bundle bundle)
		//        {
		//            base.OnCreate(bundle);
		//
		//            // Create your application here
		//        }
		ImageView choosenImageView;
		Button savePicture;
		Bitmap bmp;
		Bitmap alteredBitmap;
		Canvas canvas;
		Paint paint;
		Matrix matrix;
		float downx = 0;
		float downy = 0;
		float upx = 0;
		float upy = 0;

		public override View OnCreateView( LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState )
		{
			base.OnCreateView( inflater, container, savedInstanceState );
			return inflater.Inflate( Resource.Layout.EditPhoto, null );
		}

		public override void OnViewCreated( View view, Bundle savedInstanceState )
		{
			base.OnViewCreated( view, savedInstanceState );

			choosenImageView = (ImageView) view.FindViewById( Resource.Id.ChoosenImageView );
			savePicture = (Button) view.FindViewById( Resource.Id.SavePictureButton );

			savePicture.SetOnClickListener( this );
			choosenImageView.SetOnTouchListener( this );

			bmp = (Bitmap) Arguments.GetParcelable( "image" );

			alteredBitmap = Bitmap.CreateBitmap( bmp.Width, bmp
				.Height, bmp.GetConfig() );

			canvas = new Canvas( alteredBitmap );
			paint = new Paint();
			paint.Color = ( Color.Green );
			paint.StrokeWidth = 5;
			matrix = new Matrix();
			canvas.DrawBitmap( bmp, matrix, paint );

			choosenImageView.SetImageBitmap( alteredBitmap );
			choosenImageView.SetOnTouchListener( this );


		}

		public bool OnTouch( View v, MotionEvent ev )
		{
			MotionEventActions action = ev.Action;
			switch (action)
			{
			case MotionEventActions.Down:

				downx = ev.GetX();
				downy = ev.GetY();
				Log.Debug( Class.SimpleName, string.Format( "Down [{0},{1}]", downx, downy ) );
				break;
			case MotionEventActions.Move:
				Android.Graphics.Path path = new Android.Graphics.Path();
				path.MoveTo( downx, downy );
				for( int i = 0; i < ev.HistorySize; i++ )
				{
					Log.Debug( Class.SimpleName, string.Format( "{0}: [{1},{2}]", i, ev.GetHistoricalX( i ), ev.GetHistoricalY( i ) ) );
					path.LineTo( ev.GetHistoricalX( i ), ev.GetHistoricalY( i ) );
				}
				downx = ev.GetX();
				downy = ev.GetY();
				Log.Debug( Class.SimpleName, string.Format( "Move [{0},{1}]", downx, downy ) );
				path.LineTo( downx, downy );
				canvas.DrawPath( path, paint );
				choosenImageView.Invalidate();
				break;
			case MotionEventActions.Up:
				upx = ev.GetX();
				upy = ev.GetY();
				canvas.DrawLine( downx, downy, upx, upy, paint );
				choosenImageView.Invalidate();
				break;
			case MotionEventActions.Cancel:
				break;
			default:
				break;
			}
			return true;
		}

		public void OnClick( View v )
		{
			if ( alteredBitmap != null )
			{
				ContentValues contentValues = new ContentValues( 3 );
				contentValues.Put( Android.Provider.MediaStore.Images.Media.InterfaceConsts.DisplayName, "Draw On Me" );
                    
//				Android.Net.Uri imageFileUri = ContentResolver.Insert( Android.Provider.MediaStore.Images.Media.ExternalContentUri,
//					                               contentValues );
				try
				{
//					Stream imageFileOS = ContentResolver.OpenOutputStream( imageFileUri );
//					alteredBitmap.Compress( Bitmap.CompressFormat.Jpeg, 90, imageFileOS );
					Toast t = Toast.MakeText( Activity, "Saved!", ToastLength.Short );
					t.Show();
                        
				} catch ( Exception e )
				{
					Log.Error( "EXCEPTION", e.Message );
				}
			}

		}
	}
}

