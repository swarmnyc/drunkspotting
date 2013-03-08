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
	int m_id;
	int m_template_id;
	double m_latitude;
	double m_longitude;
	NSString *m_title;
	NSString *m_description;
	int m_rating;
	int m_rating_count;
	NSString *m_url;
	NSDate *m_time_posted;
}
@property( nonatomic, copy ) NSString *description;
@property( nonatomic ) int id;
@property( nonatomic ) double latitude;
@property( nonatomic ) double longitude;
@property( nonatomic ) int rating;
@property( nonatomic ) int rating_count;
@property( nonatomic ) int template_id;
@property( nonatomic, strong ) NSDate *time_posted;
@property( nonatomic, copy ) NSString *title;
@property( nonatomic, copy ) NSString *url;


@end
