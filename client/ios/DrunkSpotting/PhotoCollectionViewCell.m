//
//  PhotoCollectionViewCell.m
//  DrunkSpotting
//
//  Created by Cameron Hendrix on 3/7/13.
//
//

#import "PhotoCollectionViewCell.h"
#import "UIImageView+AFNetworking.h"
#import "AppDelegate.h"

@interface PhotoCollectionViewCell ()

@property (strong, nonatomic) UIImageView *photoView;
@property (strong, nonatomic) UIButton *fbShareButton;

@end

@implementation PhotoCollectionViewCell

@synthesize photoView;

- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        photoView = [[UIImageView alloc] initWithFrame:[self bounds]];
        [photoView setContentMode:UIViewContentModeScaleAspectFill];
        [photoView setClipsToBounds:YES];
        [self.contentView addSubview:photoView];
        
        [[NSNotificationCenter defaultCenter] addObserver:self
                                                 selector:@selector(handleFBSessionChange)
                                                     name:FBSessionStateChangedNotification
                                                   object:nil];
        
        self.fbShareButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
        [self.fbShareButton setTitle:NSLocalizedString(@"FB", @"FB") forState:UIControlStateNormal];
        self.fbShareButton.hidden = !FBSession.activeSession.isOpen;
        
        CGRect buttonRect = self.fbShareButton.frame;
        buttonRect.origin = CGPointMake(CGRectGetMaxX(self.contentView.bounds) - 50,
                                        CGRectGetMaxY(self.contentView.bounds) - 50);
        buttonRect.size = CGSizeMake(50, 50);
        self.fbShareButton.frame = buttonRect;
        
        [self.contentView addSubview:self.fbShareButton];
    }
    return self;
}

- (void) handleFBSessionChange {
    
    self.fbShareButton.hidden = !FBSession.activeSession.isOpen;
}

- (void) setPicture:(Picture*)picture
{


	NSString *urlstring = [picture.url stringByReplacingOccurrencesOfString:@"\\" withString:@""];

	NSLog( @"%@", urlstring );

	[photoView setImageWithURL:[NSURL URLWithString:urlstring]];
}

-(UIImage *) image
{
	return self.photoView.image;
}

@end
