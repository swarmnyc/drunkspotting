//
//  TemplateServiceTest.h
//  TemplateServiceTest
//
//  Created by Adam Ritenauer on 08.03.13.
//
//

#import <SenTestingKit/SenTestingKit.h>
#import "TemplateService.h"

@interface TemplateServiceTest : SenTestCase
{
	TemplateService * m_templateService;
}
@property( nonatomic, strong ) TemplateService *templateService;


@end
