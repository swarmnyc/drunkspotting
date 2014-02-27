//
//  AppDelegate.h
//  DrunkSpotting
//
//  Created by Adam Ritenauer on 07.03.13.
//
//

#import <UIKit/UIKit.h>

extern NSString *const FBSessionStateChangedNotification;

@interface AppDelegate : UIResponder <UIApplicationDelegate>

@property (strong, nonatomic) UIWindow *window;
- (BOOL)openSessionWithAllowLoginUI:(BOOL)allowLoginUI;

@end
