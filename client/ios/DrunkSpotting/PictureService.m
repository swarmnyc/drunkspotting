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

+ (void)postTemplate:(Template*)metadata
{
    NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"http://api.drunkspotting.com/templates"]];
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL:url];
    NSData *requestData = [[metadata dictionary] JSONFromDictionary];
    
    [request setHTTPMethod:@"POST"];
    [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
    [request setValue:[NSString stringWithFormat:@"%d", [requestData length]] forHTTPHeaderField:@"Content-Length"];
    [request setHTTPBody:requestData];
    
    [NSURLConnection sendAsynchronousRequest:request queue:[NSOperationQueue mainQueue] completionHandler:^(NSURLResponse *response, NSData *data, NSError *error) {
        NSLog(@"Error.description = %@",error.description);
        NSError* serializationError = nil;
        id result = [NSJSONSerialization JSONObjectWithData:data options:kNilOptions error:&serializationError];
        
        if (!serializationError) {
            NSLog(@"result = %@",result);
        } else NSLog(@"Error serializing JSON");
        
        //NSError* serializationError = nil;
        //id result = [NSJSONSerialization JSONObjectWithData:data options:kNilOptions error:&serializationError];
        
        // TODO: Implement error handling in callback
    }];
}

+ (void)postTemplateImage:(UIImage *)image metadata:(Template*)metadata
{
    NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"http://api.drunkspotting.com/upload_template"]];
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL:url];
    NSData *requestData = UIImageJPEGRepresentation(image, 1.0);
    
    [request setHTTPMethod:@"POST"];
    [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
    [request setValue:[NSString stringWithFormat:@"%d", [requestData length]] forHTTPHeaderField:@"Content-Length"];
    [request setHTTPBody:requestData];
    
    [NSURLConnection sendAsynchronousRequest:request queue:[NSOperationQueue mainQueue] completionHandler:^(NSURLResponse *response, NSData *data, NSError *error) {
        // TODO: Implement error handling in callback
        
        NSError* serializationError = nil;
        id result = [NSJSONSerialization JSONObjectWithData:data options:kNilOptions error:&serializationError];
        
        if (!serializationError) {
            metadata.url = [result objectForKey:@"url"];
            [PictureService postTemplate:metadata];
        } else NSLog(@"Error serializing JSON");
    }];
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