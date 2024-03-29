
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
    public class PictureListViewItem : RelativeLayout
    {
        public ProgressBar ProgressBar { get; set; }

        public FadeImageView ImageView { get; set; }

        public string ImageUrl
        {
            get
            {
                return ImageView.ImageUrl;
            }
            set
            {
                ImageView.ImageUrl = value;
            }
        }

        public PictureListViewItem(Context context) :
            base (context)
        {
            Initialize();
        }

        public PictureListViewItem(Context context, IAttributeSet attrs) :
            base (context, attrs)
        {
            Initialize();
        }

        public PictureListViewItem(Context context, IAttributeSet attrs, int defStyle) :
            base (context, attrs, defStyle)
        {
            Initialize();
        }

        void Initialize()
        {
            LayoutInflater inflater = (LayoutInflater)Context.GetSystemService(Context.LayoutInflaterService);

            Rect frame = new Rect();
            this.SetBackgroundResource(Android.Resource.Color.White);

            GetWindowVisibleDisplayFrame(frame);

            inflater.Inflate(Resource.Layout.PictureListViewItem, this, true);

            ProgressBar = FindViewById<ProgressBar>(Resource.Id.progressBar);
            ImageView = FindViewById<FadeImageView>(Resource.Id.pictureImageView);

            ImageView.DownloadingImage += (sender, e) => { 
                ((Activity)Context).RunOnUiThread(() => ProgressBar.Visibility = ViewStates.Visible);};
            ImageView.DownloadedImage += (sender, e) => {
                ((Activity)Context).RunOnUiThread(() => ProgressBar.Visibility = ViewStates.Gone);};



            this.SetMinimumHeight(frame.Right);
        }

        public void CleanUp()
        {
            ImageView.CleanUp();
        }
    }
}

