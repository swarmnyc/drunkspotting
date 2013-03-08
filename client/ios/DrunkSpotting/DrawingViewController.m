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
    
    UIBarButtonItem *doneButton = [[UIBarButtonItem alloc] initWithTitle:NSLocalizedString(@"done", @"done")
                                                                   style:UIBarButtonItemStyleDone
                                                                  target:self
                                                                  action:@selector(done:)];
    self.navigationItem.rightBarButtonItem = doneButton;
    
    UIImageView *iv = [[UIImageView alloc] initWithImage:self.originalImage];
    iv.frame = CGRectMake(0,
                          0,
                          CGRectGetWidth(self.view.bounds),
                          CGRectGetWidth(self.view.bounds));
    iv.contentMode = UIViewContentModeScaleAspectFit;
    iv.backgroundColor = [UIColor redColor];
    [self.view insertSubview:iv belowSubview:self.drawingLayer];
    
    self.photoLayer = iv;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


- (void) done:(id)send {
    
    self.uploadingOverlay.hidden = NO;
    
    [self.view addSubview:self.uploadingOverlay];

    int64_t delayInSeconds = 2.0;
    dispatch_time_t popTime = dispatch_time(DISPATCH_TIME_NOW, delayInSeconds * NSEC_PER_SEC);
    dispatch_after(popTime, dispatch_get_main_queue(), ^(void){
        
        self.uploadingOverlay.hidden = YES;
        
        [self.navigationController popToRootViewControllerAnimated:YES];
    });
   
}

@end
