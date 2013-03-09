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
@property (nonatomic, strong) IBOutlet UIActivityIndicatorView *activityIndicator;
@property (nonatomic, strong) IBOutlet UIView *colorPicker;
@property (nonatomic, strong) IBOutlet UIView *burshSlider;
@property (nonatomic, strong) IBOutlet UISlider *slider;

- (id) initWithImage:(UIImage *)image;

@end
