//
//  RootViewController.m
//  DrunkSpotting
//
//  Created by Adam Ritenauer on 07.03.13.
//
//

#import "RootViewController.h"

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
	// Do any additional setup after loading the view.
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)takePhoto:(id)sender {
 
    UIImagePickerController *imgpic = [[UIImagePickerController alloc] init];
    if([UIImagePickerController isSourceTypeAvailable:UIImagePickerControllerSourceTypeCamera]) {
        imgpic.sourceType = UIImagePickerControllerSourceTypeCamera;
    }
    else {
        //REVIEW: Camerad not available
    }
    
    [self presentViewController:imgpic animated:YES completion:^{
        
    }];
    
}

@end
