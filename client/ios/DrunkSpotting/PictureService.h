//
//  Created by somya on 3/8/13.
//
//


#import <Foundation/Foundation.h>
#import "Template.h"
#import "Picture.h"

@interface PictureService : NSObject
{
	NSString * m_baseUrl;
}
@property( nonatomic, copy ) NSString *baseUrl;


- (void)getPicture:(int)pictureId success:(void (^)(Picture *))success
	failure:(void (^)(NSError *))failure;

+ (void)postTemplate:(Template*)metadata;
+ (void)postTemplateImage:(UIImage *)image metadata:(Template*)metadata;

- (void)getPictures:(int)size success:(void (^)(NSArray *))success
	failure:(void (^)(NSError *))failure;

@end