//
//  PhotoCollectionViewCell.h
//  DrunkSpotting
//
//  Created by Cameron Hendrix on 3/7/13.
//
//

#import <UIKit/UIKit.h>
#import "Picture.h"

@interface PhotoCollectionViewCell : UICollectionViewCell

@property (nonatomic, strong) Picture *picture;

- (UIImage *)image;


@end
