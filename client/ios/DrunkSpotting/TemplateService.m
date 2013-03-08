//
//  Created by somya on 3/8/13.
//
//


#import "TemplateService.h"
#import "Template.h"
#import "AFJSONRequestOperation.h"

@implementation TemplateService
@synthesize baseUrl = m_baseUrl;

- (void)postTemplate:(Template *) template
{
}

- (void) getTemplate:(NSString *)templateId success:(void (^)(Template *))success
                                        failure:(void (^)(NSError *))failure;
{
	NSURL *url = [NSURL URLWithString:templateId];
	NSURLRequest *request = [NSURLRequest requestWithURL:url];

	AFJSONRequestOperation *operation =
		[AFJSONRequestOperation JSONRequestOperationWithRequest:request
			success:^( NSURLRequest *urlRequest, NSHTTPURLResponse *response, id JSON )
			{
				Template * template = [[Template alloc] init];
				template.id =  [JSON valueForKeyPath:@"id"];

				success(template);

			} failure:nil];

	[operation start];
}


@end