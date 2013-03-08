//
//  Created by somya on 3/8/13.
//
//


#import "TemplateService.h"
#import "Template.h"
#import "AFJSONRequestOperation.h"
#import "PictureService.h"
#import "Picture.h"

@implementation PictureService
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

- (void)getPicture:(int)pictureId success:(void (^)(Picture *))success
	failure:(void (^)(NSError *))failure;
{
	NSString *path = [self.baseUrl stringByAppendingFormat:@"/templates/%d", pictureId];
	NSURL *url = [NSURL URLWithString:path];
	NSURLRequest *request = [NSURLRequest requestWithURL:url];
	AFJSONRequestOperation *operation =
		[AFJSONRequestOperation JSONRequestOperationWithRequest:request
			success:^( NSURLRequest *urlRequest, NSHTTPURLResponse *response, id JSON )
			{
				Picture *picture = [[Picture alloc] init];
				picture.id = pictureId;

				picture.description = [JSON valueForKeyPath:@"description"];
				picture.latitude = [[JSON valueForKeyPath:@"latitude"] doubleValue];
				picture.longitude = [[JSON valueForKeyPath:@"longitude"] doubleValue];
				picture.rating = [[JSON valueForKeyPath:@"rating"] integerValue];
				picture.rating_count = [[JSON valueForKeyPath:@"rating_count"] integerValue];
//				picture.time_posted =  [JSON valueForKeyPath:@"time_posted"] d;
				picture.title = [JSON valueForKeyPath:@"title"];
				picture.template_id = [[JSON valueForKeyPath:@"template_id"] integerValue];
				picture.url = [JSON valueForKeyPath:@"url"];

				success( picture );
			} failure:^( NSURLRequest *urlRequest, NSHTTPURLResponse *response, NSError *error,
			id JSON )
		{
			failure(error);
			NSLog( error );
		}];

	[operation start];
}


@end