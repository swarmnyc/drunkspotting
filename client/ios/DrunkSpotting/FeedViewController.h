//
//  FeedViewController.h
//  DrunkSpotting
//
//  Created by Cameron Hendrix on 3/7/13.
//
//

#import <UIKit/UIKit.h>

@interface FeedViewController : UIViewController <UINavigationControllerDelegate, UIImagePickerControllerDelegate>
{
	NSArray * m_pictures;
}
@property (nonatomic, strong) NSArray *pictures;
@property (nonatomic, strong) IBOutlet UIView *photoBar;


@end
