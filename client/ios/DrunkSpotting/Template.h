//
//  Created by somya on 3/8/13.
//
//


#import <Foundation/Foundation.h>

@interface Template : NSObject
{
	NSString *m_id;
	NSString *m_title;
	double m_latitude;
	double m_longitude;
	NSString *m_description;
	int m_rating;
	int m_rating_count;
	NSString *m_url;
	NSDate *m_time_posted;
}
@property( nonatomic, copy ) NSString *description;
@property( nonatomic, copy ) NSString *id;
@property( nonatomic ) double latitude;
@property( nonatomic ) double longitude;
@property( nonatomic ) int rating;
@property( nonatomic ) int rating_count;
@property( nonatomic, strong ) NSDate *time_posted;
@property( nonatomic, copy ) NSString *title;
@property( nonatomic, copy ) NSString *url;


@end