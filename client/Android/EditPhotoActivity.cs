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
using Android.Support.V4.App;
using Android;
using Android.Content.PM;
using System.Security.Cryptography;

namespace DrunkSpotting
{
	[Activity (Label = "EditPhotoActivity", Theme = "@android:style/Theme.NoTitleBar",
		ConfigurationChanges = ConfigChanges.KeyboardHidden | ConfigChanges.Orientation, ScreenOrientation = ScreenOrientation.Portrait)]			
	public class EditPhotoActivity : FragmentActivity
	{
		Button savePicture;

		Button cancelButton;

		protected override void OnCreate (Bundle savedInstanceState)
		{
			base.OnCreate (savedInstanceState);
			SetContentView (Resource.Layout.EditPhoto);
            
			savePicture = (Button)this.FindViewById (Resource.Id.btn_save);
			cancelButton = (Button)this.FindViewById (Resource.Id.btn_cancel);
            

			Intent choosePictureIntent = new Intent (
				Intent.ActionPick,
				Android.Provider.MediaStore.Images.Media.ExternalContentUri);
			StartActivityForResult (choosePictureIntent, 0);
		}

//		public void OnClick (View v)
//		{
//            
//			 if (v == savePicture) {
//                
//				if (alteredBitmap != null) {
//					ContentValues contentValues = new ContentValues (3);
//					contentValues.Put (Android.Provider.MediaStore.Images.Media.InterfaceConsts.DisplayName, "Draw On Me");
//                    
//					Android.Net.Uri imageFileUri = ContentResolver.Insert (Android.Provider.MediaStore.Images.Media.ExternalContentUri, contentValues);
//					try {
//						Stream imageFileOS = ContentResolver.OpenOutputStream (imageFileUri);
//						alteredBitmap.Compress (Bitmap.CompressFormat.Jpeg, 90, imageFileOS);
//						Toast t = Toast.MakeText (this, "Saved!", ToastLength.Short);
//						t.Show ();
//                        
//					} catch (Exception e) {
//						Log.Verbose ("EXCEPTION", e.Message);
//					}
//				}
//			}
//		}

		protected override void OnActivityResult( int requestCode, Result resultCode, Intent intent )
		{
			base.OnActivityResult( requestCode, resultCode, intent );
            
			if ( resultCode == Result.Ok )
			{
				Android.Net.Uri imageFileUri = intent.Data;
				try
				{
					BitmapFactory.Options bmpFactoryOptions = new BitmapFactory.Options();
					bmpFactoryOptions.InJustDecodeBounds = true;
					var bmp = BitmapFactory.DecodeStream( ContentResolver.OpenInputStream( imageFileUri ), null, bmpFactoryOptions );
                    
					bmpFactoryOptions.InJustDecodeBounds = false;
					bmp = BitmapFactory.DecodeStream( ContentResolver.OpenInputStream(
						imageFileUri ), null, bmpFactoryOptions );

//					SupportFragmentManager.BeginTransaction().Replace(Resource.Id.layout_content, DrawOnPhotoFragment.GetInstance(bmp)).Commit();

                    
					(FindViewById<DrawingView>(Resource.Id.layout_content)).SetBitmap(bmp);

//					var alteredBitmap = Bitmap.CreateBitmap( bmp.Width, bmp.Height, bmp.GetConfig() );

				} catch ( Exception e )
				{
					Log.Verbose( "ERROR", e.Message );
				}
			}
		}


	}
}

