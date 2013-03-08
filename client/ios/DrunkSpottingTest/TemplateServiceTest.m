//
//  TemplateServiceTest.m
//  TemplateServiceTest
//
//  Created by Adam Ritenauer on 08.03.13.
//
//

#import "TemplateServiceTest.h"

@implementation TemplateServiceTest
@synthesize templateService = m_templateService;

- (void)setUp
{
	[super setUp];

	// Set-up code here.
	self.templateService = [[TemplateService alloc] init];
}

- (void)tearDown
{
	// Tear-down code here.

	[super tearDown];
}

- (void)testGetTemplate
{
	[self.templateService getTemplate:4 success:^( Template *template )
	{
		STAssertTrue(template != nil, @"Nil template");
		CFRunLoopStop( CFRunLoopGetMain() );
	} failure:^( NSError *error )
	{
	}];

	NSLog(@"Suspending Main");
		CFRunLoopRun();
	NSLog(@"Main Resumed");
}

@end
