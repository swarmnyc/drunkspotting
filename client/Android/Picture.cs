using System;

namespace DrunkSpotting
{
	public class Picture
	{

		public int Id;
		public int Template_Id;
		public double Latitude;
		public double Longitude;
		public string Title;
		public string Description;
		public int Rating;
		public int Rating_Count;
		public string Url;
		public DateTime Time_Posted;

		public Picture ()
		{
		}
	}
}

