//
//  Picture.h
//  DrunkSpotting
//
//  Created by Somya Jain on 3/7/13.
//
//

#import <Foundation/Foundation.h>

@interface Picture : NSObject
{
	int template_id;
	int latitude;
	int longitude;
	NSString *title;
	NSString *description;
	int rating;
	int rating_count;
	NSString *url;
	NSDate *time_posted;
}

@end
