//
//  Created by somya on 3/8/13.
//
//


#import <Foundation/Foundation.h>
#import "Template.h"

@interface PictureService : NSObject
{
	NSString * m_baseUrl;
}
@property( nonatomic, copy ) NSString *baseUrl;

- (void)postTemplate:(Template *)template;

- (void)getPicture:(int)pictureId success:(void (^)(Template *))success
	failure:(void (^)(NSError *))failure;


@end