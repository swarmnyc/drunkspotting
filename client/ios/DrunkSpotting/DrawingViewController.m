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

@property( nonatomic, strong ) UIImage *originalImage;

@end

@implementation DrawingViewController

- (id)initWithImage:(UIImage *)image
{

	self = [super init];
	if ( self )
	{

		self.originalImage = image;
	}
	return self;
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
	self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
	if ( self )
	{
		// Custom initialization
	}
	return self;
}

- (void)viewDidLoad
{
	[super viewDidLoad];

	self.navigationItem.titleView =
		[[UIImageView alloc] initWithImage:[UIImage imageNamed:@"titleTreatment"]];

	self.title = @"Drunk Spotting";

	self.uploadingOverlay.hidden = YES;

	UIBarButtonItem *doneButton = [[UIBarButtonItem alloc]
		initWithTitle:NSLocalizedString(@"Save", @"Save") style:UIBarButtonItemStyleDone target:self
		action:@selector(done:)];
	UIBarButtonItem *clearButton = [[UIBarButtonItem alloc]
		initWithTitle:NSLocalizedString(@"Clear", @"Clear") style:UIBarButtonItemStyleDone
		target:self action:@selector(clear:)];
	self.navigationItem.rightBarButtonItems = @[doneButton, clearButton];

	UIImageView *iv = [[UIImageView alloc] initWithImage:self.originalImage];
	CGFloat smallestEdge =
		MIN(CGRectGetWidth( self.view.bounds ), MIN( self.originalImage.size.width,
			self.originalImage.size.height ));

	iv.frame = CGRectMake( 0, 0, smallestEdge, smallestEdge );
	iv.contentMode = UIViewContentModeScaleAspectFill;
	iv.backgroundColor = [UIColor redColor];
	[self.compositView insertSubview:iv belowSubview:self.drawingLayer];

	self.photoLayer = iv;

	self.slider.value = self.drawingLayer.lineWidth;
}

- (void)didReceiveMemoryWarning
{
	[super didReceiveMemoryWarning];
	// Dispose of any resources that can be recreated.
}

- (void)done:(id)send
{

	self.uploadingOverlay.hidden = NO;
	[self.activityIndicator startAnimating];

	UIImage *renderedImage = [self renderImage];
	NSData *jpegData = UIImageJPEGRepresentation( renderedImage, 1 );

//    int64_t delayInSeconds = 2.0;
//    dispatch_time_t popTime = dispatch_time(DISPATCH_TIME_NOW, delayInSeconds * NSEC_PER_SEC);
//    dispatch_after(popTime, dispatch_get_main_queue(), ^(void){
//
//        self.uploadingOverlay.hidden = YES;
//        [self.activityIndicator stopAnimating];
//
//        [self.navigationController popToRootViewControllerAnimated:YES];
//    });

	// TEST CODE ONLY
	Picture *picture = [[Picture alloc] init];
//	            picture.longitude = 40.732766;
//	            picture.latitude = -73.988252;
	picture.description = @"";
	picture.title = @"";
	picture.template_id = 0;

	[PictureService postImage:renderedImage type:@"picture" success:^( NSString *urlString )
	{
		picture.url = urlString;
		[PictureService postMetadata:picture type:@"picture"];
		self.uploadingOverlay.hidden = YES;
		[self.activityIndicator stopAnimating];

		[self.navigationController popToRootViewControllerAnimated:YES];
	} failure:^( NSError *error )
	{
		// ERROR HANDLING
		NSLog( @"Error = %@", error.description );
	}];
}

- (void)clear:(id)sender
{

	[self.drawingLayer clear];
}

- (UIImage *)renderImage
{

	UIGraphicsBeginImageContextWithOptions( self.compositView.bounds.size, self.compositView.opaque,
		[[UIScreen mainScreen] scale] );
	[self.compositView.layer renderInContext:UIGraphicsGetCurrentContext()];
	UIImage *img = UIGraphicsGetImageFromCurrentImageContext();
	UIGraphicsEndImageContext();
	return img;
}

- (IBAction)setWhiteColor:(id)sender
{

	self.drawingLayer.lineColor = [UIColor whiteColor];
}

- (IBAction)setBlueColor:(id)sender
{

	self.drawingLayer.lineColor = [UIColor blueColor];
}

- (IBAction)setCyanColor:(id)sender
{

	self.drawingLayer.lineColor = [UIColor cyanColor];
}

- (IBAction)setMagentaColor:(id)sender
{

	self.drawingLayer.lineColor = [UIColor magentaColor];
}

- (IBAction)setOrangeColor:(id)sender
{

	self.drawingLayer.lineColor = [UIColor orangeColor];
}

- (IBAction)setPurpleColor:(id)sender
{

	self.drawingLayer.lineColor = [UIColor purpleColor];
}

- (IBAction)setRedColor:(id)sender
{

	self.drawingLayer.lineColor = [UIColor redColor];
}

- (IBAction)setYellowColor:(id)sender
{

	self.drawingLayer.lineColor = [UIColor yellowColor];
}

- (IBAction)setGreenColor:(id)sender
{

	self.drawingLayer.lineColor = [UIColor greenColor];
}

- (IBAction)setBlackColor:(id)sender
{

	self.drawingLayer.lineColor = [UIColor blackColor];
}

- (IBAction)changeLineWidth:(UISlider *)sender
{

	self.drawingLayer.lineWidth = sender.value;
}


@end
