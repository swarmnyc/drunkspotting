//
//  Created by somya on 3/8/13.
//
//


#import "Template.h"

@implementation Template

@synthesize description = m_description;
@synthesize id = m_id;
@synthesize latitude = m_latitude;
@synthesize longitude = m_longitude;
@synthesize rating = m_rating;
@synthesize rating_count = m_rating_count;
@synthesize time_posted = m_time_posted;
@synthesize title = m_title;
@synthesize url = m_url;

-(NSDictionary*) dictionary
{
    NSMutableDictionary *dictionary = [NSMutableDictionary dictionary];
    
    if (self.title) [dictionary setObject:self.title forKey:@"title"];
    if (self.latitude) [dictionary setObject:[NSNumber numberWithDouble:self.latitude] forKey:@"latitude"];
    if (self.longitude) [dictionary setObject:[NSNumber numberWithDouble:self.longitude] forKey:@"longitude"];
    if (self.description) [dictionary setObject:self.description forKey:@"description"];
    if (self.url) [dictionary setObject:self.url forKey:@"url"];

    return dictionary;
}

@end