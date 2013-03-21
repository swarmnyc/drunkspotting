//
//  Created by somya on 3/8/13.
//
//


#import "TemplateService.h"
#import "Template.h"
#import "AFJSONRequestOperation.h"

@implementation TemplateService
@synthesize baseUrl = m_baseUrl;

- (id)init
{
	self = [super init];
	if ( self )
	{
		self.baseUrl = @"http://api.drunkspotting.com";
	}

	return self;
}

- (void)postTemplate:(Template *)template
{
}

- (void)postTemplateIamge:(UIImage *)aTemplateImage
{
}

- (void)getTemplate:(int)templateId success:(void (^)(Template *))success
	failure:(void (^)(NSError *))failure;
{
	NSString *path = [self.baseUrl stringByAppendingFormat:@"/templates/%d", templateId];
	NSURL *url = [NSURL URLWithString:path];
	NSURLRequest *request = [NSURLRequest requestWithURL:url];
	AFJSONRequestOperation *operation =
		[AFJSONRequestOperation JSONRequestOperationWithRequest:request
			success:^( NSURLRequest *urlRequest, NSHTTPURLResponse *response, id JSON )
			{
				Template *template = [[Template alloc] init];
				template.id = templateId;

				template.description = [JSON valueForKeyPath:@"description"];
				template.latitude = [[JSON valueForKeyPath:@"latitude"] doubleValue];
				template.longitude = [[JSON valueForKeyPath:@"longitude"] doubleValue];
				template.rating = [[JSON valueForKeyPath:@"rating"] integerValue];
				template.rating_count = [[JSON valueForKeyPath:@"rating_count"] integerValue];
//				template.time_posted =  [JSON valueForKeyPath:@"time_posted"] d;
				template.title = [JSON valueForKeyPath:@"title"];
				template.url = [JSON valueForKeyPath:@"url"];

				success( template );
			} failure:^( NSURLRequest *urlRequest, NSHTTPURLResponse *response, NSError *error,
			id JSON )
		{

			NSLog(@"%@", error );
			failure(error);
		}];

	[operation start];
}


@end