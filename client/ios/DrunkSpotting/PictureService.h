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

+ (void)postMetadata:(id)metadata type:(NSString*)type;
+ (void)postImage:(UIImage *)image type:(NSString*)type success:(void (^)(NSString*))success failure:(void (^)(NSError *))failure;
- (void)getPicture:(int)pictureId success:(void (^)(Picture *))success
	failure:(void (^)(NSError *))failure;
- (void)getPictures:(int)size success:(void (^)(NSArray *))success
	failure:(void (^)(NSError *))failure;

@end