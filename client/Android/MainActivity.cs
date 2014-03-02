using System;

using Android.App;
using Android.Content;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using Android.OS;
using System.Collections.Generic;
using Android;
using Android.Graphics;
using Android.Content.PM;
using Android.Support.V4.App;
using Android.Content.Res;

namespace DrunkSpotting
{
	[Activity (Label = "Drunk Spotting", Theme = "@android:style/Theme.NoTitleBar",
	           ConfigurationChanges = ConfigChanges.KeyboardHidden | ConfigChanges.Orientation, ScreenOrientation = ScreenOrientation.Portrait)]
	//ConfigurationChanges="keyboardHidden|orientation"
	public class MainActivity : FragmentActivity
	{

		private ListView photoList = null;
		private PhotoAdapter photoListAdatper = null;

		protected override void OnCreate (Bundle bundle)
		{
			base.OnCreate (bundle);

			// Set our view from the "main" layout resource
			SetContentView (Resource.Layout.Main);

			photoList = FindViewById<ListView> (Resource.Id.photoList);
			ImageButton refreshButton = FindViewById<ImageButton> (Resource.Id.btn_refresh);
			ImageButton takePhotoButton = FindViewById<ImageButton> (Resource.Id.btn_photo);

            photoListAdatper = new PhotoAdapter (this);			
			refreshButton.Click += delegate {

                photoListAdatper.Refresh();
			};


			
			photoList.Adapter = photoListAdatper;

			takePhotoButton.Click += (object sender, EventArgs e) => {
				StartActivity( typeof(EditPhotoActivity));

			};
		}

		protected override void OnResume ()
		{
			base.OnResume ();

			// Reload Items
			photoListAdatper.Refresh ();

		}

	}

	public class PhotoAdapter : BaseAdapter<Picture>
	{

		private PictureService _pictureService = new PictureService ();

		private List<Picture> _pictures = null;

		public Context Context { get; set; }

		public PhotoAdapter (Context context)
		{
			this.Context = context;
			_pictures = new List<Picture> ();
		}

		public async void Refresh ()
		{
			

            var result = await _pictureService.GetLatestPicturesAsync(20);


                if (null != result && result.Count > 0) {
                    _pictures = result;
                    ((Activity)this.Context).RunOnUiThread (() => {
                        this.NotifyDataSetChanged ();
                    });
                    
                }
                
//            });
			
		}

		public override Picture this [int position] {
			get {
				return _pictures [position];
			}
		}

		public override long GetItemId (int position)
		{
			return _pictures [position].Id;
		}

		public override View GetView (int position, View convertView, ViewGroup parent)
		{
			View view = convertView; // re-use an existing view, if one is supplied
			if (view == null) 
			{ // otherwise create a new one
				view = new PictureListViewItem (Context);
				view.LayoutParameters = new AbsListView.LayoutParams (ViewGroup.LayoutParams.FillParent, ViewGroup.LayoutParams.WrapContent);
			}
			else
			{
				((PictureListViewItem)view).CleanUp();
			}

			// set view properties to reflect data for the given row
			((PictureListViewItem)view).ImageUrl = _pictures [position].Url;
			// return the view, populated with data, for display
			return view;
		}

		public override int ViewTypeCount 
		{
			get 
			{
				return 1;
			}
		}

		public override int Count {
			get {
				return _pictures.Count;
			}
		}
	}
}

