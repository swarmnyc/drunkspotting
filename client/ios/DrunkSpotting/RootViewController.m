//
//  RootViewController.m
//  DrunkSpotting
//
//  Created by Adam Ritenauer on 07.03.13.
//
//

#import "RootViewController.h"
#import "DrawingViewController.h"

@interface RootViewController ()

@end

@implementation RootViewController

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
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)takePhoto:(id)sender {
 
    UIImagePickerController *imgpic = [[UIImagePickerController alloc] init];
    imgpic.delegate = self;
    imgpic.allowsEditing = YES;
    
    if([UIImagePickerController isSourceTypeAvailable:UIImagePickerControllerSourceTypeCamera]) {
        imgpic.sourceType = UIImagePickerControllerSourceTypeCamera;
    }
    else {
        //REVIEW: Camerad not available
    }
    
    [self presentViewController:imgpic animated:YES completion:nil];
    
}

@end
