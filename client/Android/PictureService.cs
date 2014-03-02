using System;
using System.Collections.Generic;
using System.Net;
using System.Json;
using System.Linq;
using System.Threading.Tasks;

namespace DrunkSpotting
{
    public class PictureService
    {
        public PictureService()
        {
        }

		//        public const string BASE_URL = "http://api.drunkspotting.com";
		public const string BASE_URL = "http://162.209.4.59";
        public const string LATEST_PICTURES_PATH = "pictures/latest";

		public void GetLatestPictures(int count, Action<List<Picture>> onSuccess)
		{
			onSuccess (new List<Picture> () {
				new Picture () { Id = 1, Url = "http://placekitten.com/600/480" },
				new Picture () {
					Id = 2,
					Url = "http://placedog.com/600/480"
				}
			});
		}

//        public void GetLatestPictures(int count, Action<List<Picture>> onSuccess)
//        {
//            string url = String.Format("{0}/{1}/{2}", BASE_URL, LATEST_PICTURES_PATH, count);
//
//            var httpReq = (HttpWebRequest)HttpWebRequest.Create(new Uri(url));
//
//            httpReq.BeginGetResponse((ar) => {
//                var request = (HttpWebRequest)ar.AsyncState;
//                using (var response = (HttpWebResponse)request.EndGetResponse (ar))
//                {                           
//                    var s = response.GetResponseStream();
////                  var j = JsonSerializer.DeserializeFromStream<List<Picture>>(s);
//
//                    JsonArray j = (JsonArray)JsonObject.Load(s);
//
//                    var results = from result in j
//                                   let jResult = result as JsonObject
//                                   select new Picture()
//                                   {
//                        Id = jResult ["id"],
//                        Url = jResult ["url"]
//                    };
//                    onSuccess(results.ToList());
//                }
//
//            }, httpReq);
//
//        }

        public async Task<List<Picture>> GetLatestPicturesAsync(int count)
        {
            string url = String.Format("{0}/{1}/{2}", BASE_URL, LATEST_PICTURES_PATH, count);
            
            var httpReq = (HttpWebRequest)HttpWebRequest.Create(new Uri(url));

			var response = await httpReq.GetResponseAsync();
            
			var s = response.GetResponseStream();
            //                  var j = JsonSerializer.DeserializeFromStream<List<Picture>>(s);
                    
            JsonArray j = (JsonArray)JsonObject.Load(s);
                    
            var results = from result in j
                        let jResult = result as JsonObject
                            select new Picture()
                        {
                            Id = jResult ["id"],
                            Url = jResult ["url"]
                        };
            return results.ToList();

        }
    }
}

