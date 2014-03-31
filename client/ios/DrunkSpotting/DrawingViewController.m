//
//  DrawingViewController.m
//  DrunkSpotting
//
//  Created by Adam Ritenauer on 07.03.13.
//
//

#import "DrawingViewController.h"
#import "PictureService.h"

@interface DrawingViewController ()

@property(nonatomic, strong) UIImage *originalImage;

@end


@implementation DrawingViewController

- (id)initWithImage:(UIImage *)image {

    self = [super init];
    if (self) {

        self.originalImage = image;
    }
    return self;
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}



- (void)viewDidLoad {
    [super viewDidLoad];


    [self setEdgesForExtendedLayout:UIRectEdgeNone];
    
    self.uploadingOverlay.hidden = YES;

    UIBarButtonItem *saveButton = [[UIBarButtonItem alloc] initWithTitle:NSLocalizedString(@"Save", @"Save")
                                                                   style:UIBarButtonItemStyleDone
                                                                  target:self
                                                                  action:@selector(done:)];
    saveButton.tintColor = UIColorFromRGB(0x2fcd83);
    self.navigationItem.rightBarButtonItems = @[saveButton];

    UIBarButtonItem *cancelButton = [[UIBarButtonItem alloc] initWithTitle:NSLocalizedString(@"Cancel", @"Cancel")
                                                                     style:UIBarButtonItemStyleDone
                                                                    target:self
                                                                    action:@selector(cancel:)];
    self.navigationItem.leftBarButtonItems = @[cancelButton];

    UIImageView *iv = [[UIImageView alloc] initWithImage:self.originalImage];

    CGFloat smallestEdge = 320;
    
    
//    CGFloat smallestEdge = MIN(CGRectGetWidth(self.view.bounds), MIN(self.originalImage.size.width, self.originalImage.size.height));


    iv.frame = CGRectMake(0, 0, smallestEdge, smallestEdge);
    iv.contentMode =  UIViewContentModeScaleAspectFill;
    iv.backgroundColor = [UIColor redColor];
    [self.compositView insertSubview:iv belowSubview:self.drawingLayer];
    self.compositView.clipsToBounds = YES;



    int  colors [] =    {
        0xc60000,
        0xe87b18,
        0xffcc00,
        0x16b228,
        0x0c7cc1,
        0x00b2c9,
        0x000000,
        0xffffff,
        0x3a290c,
        0xe2b574,
        0xfc00c7,
        0x8a37e2};
    
    for (int i = 0; i< 12; i++) {
        UIColor *color = UIColorFromRGB(colors[i]);
        UIButton * button = [self.colorPicker.subviews objectAtIndex:i];
        [button setBackgroundColor:color];
        [button setTag:colors[i]];
    }
    

    self.photoLayer = iv;

    self.slider.value = self.drawingLayer.lineWidth;
}

- (void)viewDidLayoutSubviews {
//    [self.compositView setFrame:CGRectMake(0, 0, [[UIScreen mainScreen] bounds].size.width, [[UIScreen mainScreen] bounds].size.width)];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void)done:(id)send {

    self.navigationItem.leftBarButtonItem.enabled = NO;

    self.uploadingOverlay.hidden = NO;
    [self.activityIndicator startAnimating];

    UIImage *renderedImage = [self renderImage];
//    NSData *jpegData = UIImageJPEGRepresentation(renderedImage, 1);

    Picture *picture = [[Picture alloc] init];
    //	            picture.longitude = 40.732766;
    //	            picture.latitude = -73.988252;
    picture.description = @"";
    picture.title = @"";
    picture.template_id = 0;

    [PictureService postImage:renderedImage type:@"picture" success:^(NSString *urlString) {
        NSLog(@"urlString = %@", urlString);
        picture.url = urlString;
        [PictureService postMetadata:picture type:@"picture"];
        self.uploadingOverlay.hidden = YES;
        [self.activityIndicator stopAnimating];

        [self.navigationController popToRootViewControllerAnimated:YES];
    }                 failure:^(NSError *error) {
        // ERROR HANDLING
        NSLog(@"Error = %@", error.description);
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Failed to save drunk spot"
                                                        message:@"Please try again"
                                                       delegate:nil
                                              cancelButtonTitle:@"OK"
                                              otherButtonTitles:nil];
        self.uploadingOverlay.hidden = YES;
        [self.activityIndicator stopAnimating];
        [alert show];
    }];
}

- (void)cancel:(id)send {

    [self.navigationController popToRootViewControllerAnimated:YES];
    return;
}

- (IBAction)undo:(id)sender {

    [self.drawingLayer undoLatestStep];
}

- (IBAction)redo:(id)sender {

    [self.drawingLayer redoLatestStep];
}

- (IBAction)showBrushSlider:(id)sender {

    self.burshSlider.hidden = !self.burshSlider.hidden;
    self.colorPicker.hidden = YES;
}

- (IBAction)showColorPicker:(id)sender {

    self.colorPicker.hidden = !self.colorPicker.hidden;
    self.burshSlider.hidden = YES;

}

- (UIImage *)renderImage {
    UIGraphicsBeginImageContextWithOptions(self.compositView.bounds.size, self.compositView.opaque,
            [[UIScreen mainScreen] scale]);
    [self.compositView.layer renderInContext:UIGraphicsGetCurrentContext()];
    UIImage *img = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return img;
}


- (IBAction)setColor:(id)sender {

    UIButton *button = sender;
    self.drawingLayer.lineColor = UIColorFromRGB([button tag]);
    self.colorPicker.hidden = YES;
}
- (IBAction)dismissBrushSlider:(id)sender {

    self.burshSlider.hidden = YES;
}

- (IBAction)changeLineWidth:(UISlider *)sender {

    self.drawingLayer.lineWidth = sender.value;
}

- (IBAction)tap:(id)sender {

}


@end
