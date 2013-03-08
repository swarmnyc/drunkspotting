//
//  DrawingViewController.h
//  DrunkSpotting
//
//  Created by Adam Ritenauer on 07.03.13.
//
//

#import <UIKit/UIKit.h>
#import "ACEDrawingView.h"

@interface DrawingViewController : UIViewController

@property (nonatomic, strong) IBOutlet UIImageView *photoLayer;
@property (nonatomic, strong) IBOutlet ACEDrawingView *drawingLayer;
@property (nonatomic, strong) IBOutlet UIView *compositView;
@property (nonatomic, strong) IBOutlet UIView *uploadingOverlay;

- (id) initWithImage:(UIImage *)image;

@end
