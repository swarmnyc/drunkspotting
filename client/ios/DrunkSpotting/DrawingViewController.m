//
//  DrawingViewController.m
//  DrunkSpotting
//
//  Created by Adam Ritenauer on 07.03.13.
//
//

#import "DrawingViewController.h"

@interface DrawingViewController ()

@property (nonatomic, strong) UIImage *originalImage;

@end

@implementation DrawingViewController


- (id) initWithImage:(UIImage *)image {
    
    self = [super init];
    if (self) {
        
        self.originalImage = image;
    }
    return self;
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    self.uploadingOverlay.hidden = YES;
    
    UIBarButtonItem *doneButton = [[UIBarButtonItem alloc] initWithTitle:NSLocalizedString(@"Save", @"Save")
                                                                   style:UIBarButtonItemStyleDone
                                                                  target:self
                                                                  action:@selector(done:)];
    UIBarButtonItem *clearButton = [[UIBarButtonItem alloc] initWithTitle:NSLocalizedString(@"Clear", @"Clear")
                                                                   style:UIBarButtonItemStyleDone
                                                                  target:self
                                                                  action:@selector(clear:)];
    self.navigationItem.rightBarButtonItems = @[doneButton, clearButton];
    
    UIImageView *iv = [[UIImageView alloc] initWithImage:self.originalImage];
    
    CGFloat smallestEdge = MIN(CGRectGetWidth(self.view.bounds), MIN(self.originalImage.size.width, self.originalImage.size.height));

    iv.frame = CGRectMake(0, 0, smallestEdge, smallestEdge);
    iv.contentMode = UIViewContentModeScaleAspectFill;
    iv.backgroundColor = [UIColor redColor];
    [self.compositView insertSubview:iv belowSubview:self.drawingLayer];
    
    self.photoLayer = iv;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


- (void) done:(id)send {
    
    self.uploadingOverlay.hidden = NO;
    [self.activityIndicator startAnimating];
    
    UIImage *renderedImage = [self renderImage];
    NSData *jpegData = UIImageJPEGRepresentation(renderedImage, 1);
    
    int64_t delayInSeconds = 2.0;
    dispatch_time_t popTime = dispatch_time(DISPATCH_TIME_NOW, delayInSeconds * NSEC_PER_SEC);
    dispatch_after(popTime, dispatch_get_main_queue(), ^(void){
        
        self.uploadingOverlay.hidden = YES;
        [self.activityIndicator stopAnimating];
        
        [self.navigationController popToRootViewControllerAnimated:YES];
    });
}

- (void) clear:(id)sender {
    
    [self.drawingLayer clear];
}

- (UIImage *) renderImage {
    
    UIGraphicsBeginImageContextWithOptions(self.compositView.bounds.size, self.compositView.opaque, [[UIScreen mainScreen] scale]);
    [self.compositView.layer renderInContext:UIGraphicsGetCurrentContext()];
    UIImage * img = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return img;
}


@end
