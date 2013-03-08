//
//  PhotoCollectionViewCell.m
//  DrunkSpotting
//
//  Created by Cameron Hendrix on 3/7/13.
//
//

#import "PhotoCollectionViewCell.h"

@interface PhotoCollectionViewCell ()

@property (strong, nonatomic) UIImageView *photoView;

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
        [self addSubview:photoView];
    }
    return self;
}

- (void) setPhoto:(UIImage*)photo
{
    [photoView setImage:photo];
}

@end
