//
//  Created by somya on 3/8/13.
//
//


#import <Foundation/Foundation.h>
#import "Template.h"

@interface TemplateService : NSObject
{
	NSString * m_baseUrl;
}
@property( nonatomic, copy ) NSString *baseUrl;

- (void)postTemplate:(Template *)template;

- (void)getTemplate:(NSString *)templateId success:(void (^)(Template *))success
	failure:(void (^)(NSError *))failure;


@end