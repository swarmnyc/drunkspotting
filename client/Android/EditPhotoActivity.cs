
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


namespace DrunkSpotting
{
    [Activity (Label = "EditPhotoActivity")]			
    public class EditPhotoActivity : Activity, View.IOnTouchListener, View.IOnClickListener
    {
//        protected override void OnCreate(Bundle bundle)
//        {
//            base.OnCreate(bundle);
//
//            // Create your application here
//        }


        ImageView choosenImageView;
        Button choosePicture;
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
        

        protected override void OnCreate(Bundle savedInstanceState) {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.EditPhoto);
            
            choosenImageView = (ImageView) this.FindViewById(Resource.Id.ChoosenImageView);
            choosePicture = (Button) this.FindViewById(Resource.Id.ChoosePictureButton);
            savePicture = (Button) this.FindViewById(Resource.Id.SavePictureButton);
            
            savePicture.SetOnClickListener(this);
            choosePicture.SetOnClickListener(this);
            choosenImageView.SetOnTouchListener(this);
        }
        
        public void OnClick(View v) {
            
            if (v == choosePicture) {
                Intent choosePictureIntent = new Intent(
                    Intent.ActionPick,
                    Android.Provider.MediaStore.Images.Media.ExternalContentUri);
                StartActivityForResult(choosePictureIntent, 0);
            } else if (v == savePicture) {
                
                if (alteredBitmap != null) {
                    ContentValues contentValues = new ContentValues(3);
                    contentValues.Put(Android.Provider.MediaStore.Images.Media.InterfaceConsts.DisplayName, "Draw On Me");
                    
                    Android.Net.Uri imageFileUri = ContentResolver.Insert(Android.Provider.MediaStore.Images.Media.ExternalContentUri, contentValues);
                    try {
                        Stream imageFileOS = ContentResolver.OpenOutputStream(imageFileUri);
                        alteredBitmap.Compress(Bitmap.CompressFormat.Jpeg, 90, imageFileOS);
                        Toast t = Toast.MakeText(this, "Saved!", ToastLength.Short);
                        t.Show();
                        
                    } catch (Exception e) {
                        Log.Verbose("EXCEPTION", e.Message);
                    }
                }
            }
        }
        
        protected override void OnActivityResult(int requestCode, Result resultCode,
                                        Intent intent) {
            base.OnActivityResult(requestCode, resultCode, intent);
            
            if (resultCode == Result.Ok) {
                Android.Net.Uri imageFileUri = intent.Data;
                try {
                    BitmapFactory.Options bmpFactoryOptions = new BitmapFactory.Options();
                    bmpFactoryOptions.InJustDecodeBounds = true;
                    bmp = BitmapFactory.DecodeStream(ContentResolver.OpenInputStream(
                        imageFileUri), null, bmpFactoryOptions);
                    
                    bmpFactoryOptions.InJustDecodeBounds = false;
                    bmp = BitmapFactory.DecodeStream(ContentResolver.OpenInputStream(
                        imageFileUri), null, bmpFactoryOptions);
                    
                    alteredBitmap = Bitmap.CreateBitmap(bmp.Width, bmp
                                                        .Height, bmp.GetConfig());
                    canvas = new Canvas(alteredBitmap);
                    paint = new Paint();
                    paint.Color = (Color.Green);
                    paint.StrokeWidth = 5;
                    matrix = new Matrix();
                    canvas.DrawBitmap(bmp, matrix, paint);

                    choosenImageView.SetImageBitmap(alteredBitmap);
                    choosenImageView.SetOnTouchListener(this);
                } catch (Exception e) {
                    Log.Verbose("ERROR", e.Message);
                }
            }
        }
        public bool OnTouch(View v, MotionEvent @event) {
            MotionEventActions action = @event.Action;
            switch (action) {
                case MotionEventActions.Down:
                    downx = @event.GetX();
                    downy = @event.GetY();
                    break;
                case MotionEventActions.Move:
                    upx = @event.GetX();
                    upy = @event.GetY();
                    canvas.DrawLine(downx, downy, upx, upy, paint);
                    choosenImageView.Invalidate();
                    downx = upx;
                    downy = upy;
                    break;
                case MotionEventActions.Up:
                    upx = @event.GetX();
                    upy = @event.GetY();
                    canvas.DrawLine(downx, downy, upx, upy, paint);
                    choosenImageView.Invalidate();
                    break;
                case MotionEventActions.Cancel:
                    break;
                default:
                    break;
            }
            return true;
        }

    }
}

