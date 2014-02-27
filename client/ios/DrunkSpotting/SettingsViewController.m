//
//  SettingsViewController.m
//  DrunkSpotting
//
//  Created by Adam Ritenauer on 28.03.13.
//
//

#import "SettingsViewController.h"
#import "AppDelegate.h"

@interface SettingsViewController ()

@end

@implementation SettingsViewController

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
    // Do any additional setup after loading the view from its nib.
}

- (void)viewDidAppear:(BOOL)animated {
    
    self.toggleFBButton.selected = FBSession.activeSession.isOpen;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

-(IBAction) toggleFBAuth:(UIButton *)sender {
    if(FBSession.activeSession.isOpen){
        [FBSession.activeSession closeAndClearTokenInformation];
    }
    else {
        AppDelegate *appDelegate = [[UIApplication sharedApplication] delegate];
        // The user has initiated a login, so call the openSession method
        // and show the login UX if necessary.
        [appDelegate openSessionWithAllowLoginUI:YES];
    }
}

@end
