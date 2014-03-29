//
//  FeedViewController.m
//  DrunkSpotting
//
//  Created by Cameron Hendrix on 3/7/13.
//
//

#import "FeedViewController.h"
#import "PhotoCollectionViewCell.h"
#import "DrawingViewController.h"
#import "TemplateService.h"
#import "PictureService.h"
#import "AppDelegate.h"
#import "SettingsViewController.h"

#import "Template.h"

NSString *const kPhotoCellIdentifier = @"photo";

@interface FeedViewController () <UICollectionViewDataSource, UICollectionViewDelegate, UIActionSheetDelegate>

@property( strong, nonatomic ) UICollectionView *feedView;
@property( strong, nonatomic ) UIRefreshControl *refreshControl;


@end

@implementation FeedViewController

@synthesize feedView;
@synthesize refreshControl;

@synthesize pictures = m_pictures;

- (void)viewDidLoad
{
    UIColor *teal = UIColorFromRGB(0x00b2c9);
    self.navigationController.navigationBar.tintColor=teal;
    self.navigationItem.title = @"drunkspotting";
    
	[self refreshList];
}

- (void)viewDidLayoutSubviews
{
    
	feedView = [[UICollectionView alloc]
		initWithFrame:CGRectMake(0, 0, CGRectGetWidth(self.view.bounds), CGRectGetHeight(self.view.bounds))
		collectionViewLayout:[[UICollectionViewFlowLayout alloc] init]];
    
	[feedView registerClass:[PhotoCollectionViewCell class]
		forCellWithReuseIdentifier:kPhotoCellIdentifier];
	[feedView setBackgroundColor:[UIColor whiteColor]];
	[feedView setDelegate:self];
	[feedView setDataSource:self];
    [self.view addSubview:feedView ];
   
    
    UIRefreshControl *refresh = [[UIRefreshControl alloc] init];
    refresh.attributedTitle = [[NSAttributedString alloc] initWithString:@"Pull to Refresh"];
    [refresh addTarget:self action:@selector(refreshList) forControlEvents:UIControlEventValueChanged];
    self.refreshControl = refresh;
    
    [feedView addSubview:self.refreshControl];
    [feedView reloadData];

//
//	UIBarButtonItem *refreshButton = [[UIBarButtonItem alloc]
//		initWithBarButtonSystemItem:UIBarButtonSystemItemRefresh target:self action:@selector(refreshList:)];
//	self.navigationItem.rightBarButtonItems = @[refreshButton];
    
//    UIBarButtonItem *settingsButton = [[UIBarButtonItem alloc]
//                                      initWithTitle:NSLocalizedString(@"Settings",@"Settings") style:UIBarButtonItemStylePlain target:self action:@selector(openSettings:)];
//	self.navigationItem.leftBarButtonItems = @[settingsButton];
    
    self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithImage:[UIImage imageNamed:@"camera.png"] style:UIBarButtonItemStylePlain target:self action:@selector(onCamera)];
}

- (void)stopRefresh { [self.refreshControl endRefreshing]; }

- (void)refreshList
{
	PictureService *pictureService = [[PictureService alloc] init];
		[pictureService getPictures:20 success:^( NSArray *array )
		{
			self.pictures = array;
			[self.feedView reloadData];
            [self performSelector:@selector(stopRefresh) withObject:self afterDelay:2.5];
        } failure:^( NSError *error )
		{
			NSLog(@"%@", error );
		}];
}

- (void)openSettings:(id)refreshList {
    
    SettingsViewController *svc = [[SettingsViewController alloc] init];
    [self.navigationController pushViewController:svc animated:YES];
}

- (void) viewDidAppear:(BOOL)animated
{
    //[self testPostImage];
}

- (void)testApp
{
	PictureService *pictureService = [[PictureService alloc] init];

	[pictureService getPicture:6 success:^( Picture *t )
	{
		NSLog(@"%@", t.description );
	} failure:^( NSError *error )
	{
		NSLog(@"%@", error );
	}];
}

- (void)onCamera
{
    UIActionSheet *addItemAction = [[UIActionSheet alloc] initWithTitle:nil delegate:self cancelButtonTitle:@"Cancel" destructiveButtonTitle:nil otherButtonTitles:@"Camera", @"Photo Library", nil];

    if ([UIImagePickerController isSourceTypeAvailable:UIImagePickerControllerSourceTypeCamera]) {
        [addItemAction showInView:self.view  ];
	} else {
        // Go straight to the Photo Library
        [self actionSheet:addItemAction clickedButtonAtIndex:1];
    }
}

- (void)actionSheet:(UIActionSheet *)actionSheet clickedButtonAtIndex:(NSInteger)buttonIndex
{
    if ([[actionSheet buttonTitleAtIndex:buttonIndex] isEqualToString:@"Cancel"]) return;

    UIImagePickerController *imgpic = [[UIImagePickerController alloc] init];
	imgpic.delegate = self;
//	imgpic.allowsEditing = YES;

    if ([[actionSheet buttonTitleAtIndex:buttonIndex] isEqualToString:@"Camera"]) {
        imgpic.sourceType = UIImagePickerControllerSourceTypeCamera;
    } else if ([[actionSheet buttonTitleAtIndex:buttonIndex] isEqualToString:@"Photo Library"]) {
        imgpic.sourceType = UIImagePickerControllerSourceTypePhotoLibrary;
    }
    
    [self presentViewController:imgpic animated:YES completion:nil];
}

#pragma mark - <UICollectionViewDatasource>

- (NSInteger)collectionView:(UICollectionView *)view numberOfItemsInSection:(NSInteger)section;
{
	return [self.pictures count];
}

- (NSInteger)numberOfSectionsInCollectionView:(UICollectionView *)collectionView
{
	return 1;
}

- (UICollectionViewCell *)collectionView:(UICollectionView *)cv
	cellForItemAtIndexPath:(NSIndexPath *)indexPath;
{
	PhotoCollectionViewCell *cell =
		[cv dequeueReusableCellWithReuseIdentifier:kPhotoCellIdentifier forIndexPath:indexPath];
	[cell setPicture:[self.pictures objectAtIndex:indexPath.row]];

	return cell;
}

#pragma mark - <UICollectionViewFlowLayoutDelegate>

- (void)collectionView:(UICollectionView *)collectionView
	didSelectItemAtIndexPath:(NSIndexPath *)indexPath
{
    return;
}

- (CGSize)collectionView:(UICollectionView *)collectionView
	layout:(UICollectionViewLayout *)collectionViewLayout
	sizeForItemAtIndexPath:(NSIndexPath *)indexPath
{
	UIEdgeInsets insets = [self collectionView:nil layout:nil insetForSectionAtIndex:0];
	CGFloat squareSideSize = [[UIScreen mainScreen] bounds].size.width - insets.left - insets.right;
	return CGSizeMake( squareSideSize, squareSideSize );
}

- (UIEdgeInsets)collectionView:(UICollectionView *)collectionView
	layout:(UICollectionViewLayout *)collectionViewLayout insetForSectionAtIndex:(NSInteger)section
{
	return UIEdgeInsetsMake( 10, 10, 10, 10 );
}

- (CGFloat)collectionView:(UICollectionView *)collectionView
	layout:(UICollectionViewLayout *)collectionViewLayout
	minimumLineSpacingForSectionAtIndex:(NSInteger)section
{
	return 10.f;
}

#pragma mark - <UIImagePickerControllerDelegate>

- (void)imagePickerController:(UIImagePickerController *)picker
	didFinishPickingMediaWithInfo:(NSDictionary *)info
{
	[self dismissViewControllerAnimated:YES completion:^
	{
		UIImage *pickedImage = [info objectForKey:UIImagePickerControllerOriginalImage];

		if ( pickedImage )
		{
			DrawingViewController *dvc = [[DrawingViewController alloc] initWithImage:pickedImage];
			[self.navigationController pushViewController:dvc animated:YES];
		}
	}];
}

//Tells the delegate that the user cancelled the pick operation.
- (void)imagePickerControllerDidCancel:(UIImagePickerController *)picker
{
    [self.navigationController popToRootViewControllerAnimated:YES];
    [self dismissViewControllerAnimated:YES completion:nil];
}


@end
