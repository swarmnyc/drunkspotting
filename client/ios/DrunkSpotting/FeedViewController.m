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

#import "Template.h"

NSString *const kPhotoCellIdentifier = @"photo";

@interface FeedViewController () <UICollectionViewDataSource, UICollectionViewDelegate, UIActionSheetDelegate>

@property( strong, nonatomic ) UICollectionView *feedView;

@end

@implementation FeedViewController

@synthesize feedView;
@synthesize pictures = m_pictures;

- (void)viewDidLoad
{
    self.navigationItem.titleView = [[UIImageView alloc] initWithImage:[UIImage imageNamed:@"titleTreatment"]];

	PictureService *pictureService = [[PictureService alloc] init];
	[pictureService getPictures:20 success:^( NSArray *array )
	{
		self.pictures = array;
		[self.feedView reloadData];
	} failure:^( NSError *error )
	{
		NSLog(@"%@", error );
	}];
}

- (void)viewDidLayoutSubviews
{
	feedView = [[UICollectionView alloc]
		initWithFrame:self.view.bounds
		collectionViewLayout:[[UICollectionViewFlowLayout alloc] init]];
	[feedView registerClass:[PhotoCollectionViewCell class]
		forCellWithReuseIdentifier:kPhotoCellIdentifier];
	[feedView setBackgroundColor:[UIColor whiteColor]];
	[feedView setDelegate:self];
	[feedView setDataSource:self];
	[self.view addSubview:feedView];
	[feedView reloadData];

	self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc]
                                              initWithBarButtonSystemItem:UIBarButtonSystemItemAdd target:self action:@selector(addItem:)];
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

- (void) testPostImage
{
    [self addItem:self.navigationItem.rightBarButtonItem];
}

- (void)addItem:(id)sender
{
    UIActionSheet *addItemAction = [[UIActionSheet alloc] initWithTitle:nil delegate:self cancelButtonTitle:@"Cancel" destructiveButtonTitle:nil otherButtonTitles:@"Camera", @"Photo Library", nil];

    if ([UIImagePickerController isSourceTypeAvailable:UIImagePickerControllerSourceTypeCamera]) {
        [addItemAction showFromBarButtonItem:sender animated:YES];
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
	imgpic.allowsEditing = YES;

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
		UIImage *pickedImage = [info objectForKey:UIImagePickerControllerEditedImage];

		if ( pickedImage )
		{
            // TEST CODE ONLY
            Template *testTemplate = [[Template alloc] init];
            testTemplate.longitude = 40.732766;
            testTemplate.latitude = -73.988252;
            testTemplate.description = @"Yo yo yo day 2";
            testTemplate.title = @"Hello World! day 2";

			[PictureService postImage:pickedImage type:@"template" success:^(NSString *urlString) {
                testTemplate.url = urlString;
                [PictureService postMetadata:testTemplate type:@"template"];
            } failure:^(NSError *error) {
                // ERROR HANDLING
                NSLog(@"Error = %@",error.description);
            }];
            
			//DrawingViewController *dvc = [[DrawingViewController alloc] initWithImage:pickedImage];
			//[self.navigationController pushViewController:dvc animated:YES];
		}
	}];
}

//Tells the delegate that the user cancelled the pick operation.
- (void)imagePickerControllerDidCancel:(UIImagePickerController *)picker
{
    [self dismissViewControllerAnimated:YES completion:nil];
}


@end
