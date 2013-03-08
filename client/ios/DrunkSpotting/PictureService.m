//
//  Created by somya on 3/8/13.
//
//


#import "TemplateService.h"
#import "Template.h"
#import "AFJSONRequestOperation.h"
#import "PictureService.h"
#import "Picture.h"
#import "NSDictionary+JSONCategories.h"
#import "AFHTTPClient.h"

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

+ (void)postMetadata:(id)metadata type:(NSString*)type
{
	NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"http://api.drunkspotting.com/%@s",type]];
	NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL:url];
	NSData *requestData = [[metadata dictionary] JSONFromDictionary];

	[request setHTTPMethod:@"POST"];
	[request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
	[request setValue:[NSString stringWithFormat:@"%d", [requestData length]]
		forHTTPHeaderField:@"Content-Length"];
	[request setHTTPBody:requestData];

	[NSURLConnection sendAsynchronousRequest:request queue:[NSOperationQueue mainQueue]
		completionHandler:^( NSURLResponse *response, NSData *data, NSError *error )
		{
			NSLog( @"Error.description = %@", error.description );
			NSError *serializationError = nil;
			id result = [NSJSONSerialization JSONObjectWithData:data options:kNilOptions
				error:&serializationError];

			if ( !serializationError ) {
				NSLog( @"result = %@", result );
			} else { NSLog( @"Error serializing JSON" );}
		}];
}


+ (void)postImage:(UIImage *)image type:(NSString*)type success:(void (^)(NSString*))success failure:(void (^)(NSError *))failure
{
	NSURL *url =
		[NSURL URLWithString:[NSString stringWithFormat:@"http://api.drunkspotting.com/"]];

	AFHTTPClient *httpClient = [[AFHTTPClient alloc] initWithBaseURL:url];

	NSData *imageData = UIImageJPEGRepresentation( image, 0.5 );

	NSMutableURLRequest *request = [httpClient multipartFormRequestWithMethod:@"POST" path:[NSString stringWithFormat:@"upload_%@",type] parameters:nil constructingBodyWithBlock: ^(id <AFMultipartFormData>formData) {
	    [formData appendPartWithFormData:imageData name:[NSString stringWithFormat:@"%@.jpg",type]];
	}];

	AFHTTPRequestOperation *operation = [[AFHTTPRequestOperation alloc] initWithRequest:request];
	[operation setUploadProgressBlock:^(NSUInteger bytesWritten, long long totalBytesWritten, long long totalBytesExpectedToWrite) {
	    NSLog(@"Sent %lld of %lld bytes", totalBytesWritten, totalBytesExpectedToWrite);
	}];
    [operation setCompletionBlockWithSuccess:^(AFHTTPRequestOperation *operation, id responseObject) {
        NSError *error = nil;
        NSDictionary *result = [NSJSONSerialization JSONObjectWithData:responseObject options:kNilOptions error:&error];
        
        success([result objectForKey:@"url"]);
    } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
        failure(error);
    }];
    [operation start];
}

- (void)getPicture:(int)pictureId success:(void (^)(Picture *))success
	failure:(void (^)(NSError *))failure;
{
	NSString *path = [self.baseUrl stringByAppendingFormat:@"/pictures/%d", pictureId];
	NSURL *url = [NSURL URLWithString:path];
	NSURLRequest *request = [NSURLRequest requestWithURL:url];
	AFJSONRequestOperation *operation =
		[AFJSONRequestOperation JSONRequestOperationWithRequest:request
			success:^( NSURLRequest *urlRequest, NSHTTPURLResponse *response, id JSON )
			{
				Picture *picture = [[Picture alloc] init];
				picture.id = pictureId;

				[self populatePicture:picture JSON:JSON];

				success( picture );
			} failure:^( NSURLRequest *urlRequest, NSHTTPURLResponse *response, NSError *error,
			id JSON )
		{
			failure(error);
			NSLog(@"%@", error);

			failure( error );
			NSLog(@"%@", error);
		}];

	[operation start];
}

- (void)getPictures:(int)size success:(void (^)(NSArray *pictues))success
	failure:(void (^)(NSError *))failure
{
	NSString *path = [self.baseUrl stringByAppendingFormat:@"/templates/latest/%d", size];
	NSURL *url = [NSURL URLWithString:path];
	NSURLRequest *request = [NSURLRequest requestWithURL:url];
	AFJSONRequestOperation *operation =
		[AFJSONRequestOperation JSONRequestOperationWithRequest:request
			success:^( NSURLRequest *urlRequest, NSHTTPURLResponse *response, id JSON )
			{
				NSMutableArray *pictures = [[NSMutableArray alloc] init];

				for ( NSDictionary *dictionary in JSON )
				{
					Picture *picture = [[Picture alloc] init];
					[self populatePicture:picture JSON:dictionary];
					[pictures addObject:picture];
				}

				success( pictures );
			} failure:^( NSURLRequest *urlRequest, NSHTTPURLResponse *response, NSError *error,
			id JSON )
		{
			failure( error);
			NSLog(@"%@", error);
		}];

	[operation start];
}

- (void)populatePicture:(Picture *)picture JSON:(id)JSON
{
	id value = [JSON valueForKeyPath:@"id"];
	if ( value )
	{
		picture.id = [value integerValue];
	}
	picture.description = [JSON valueForKeyPath:@"description"];
	picture.latitude = [[JSON valueForKeyPath:@"latitude"] doubleValue];
	picture.longitude = [[JSON valueForKeyPath:@"longitude"] doubleValue];
	picture.rating = [[JSON valueForKeyPath:@"rating"] integerValue];
	picture.rating_count = [[JSON valueForKeyPath:@"rating_count"] integerValue];
//				picture.time_posted =  [JSON valueForKeyPath:@"time_posted"] d;
	picture.title = [JSON valueForKeyPath:@"title"];
	picture.template_id = [[JSON valueForKeyPath:@"template_id"] integerValue];
	picture.url = [JSON valueForKeyPath:@"url"];
}


@end