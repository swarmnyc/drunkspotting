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

NSString *const kPhotoCellIdentifier = @"photo";

@interface FeedViewController ()
<UICollectionViewDataSource, UICollectionViewDelegate>

@property (strong, nonatomic) UICollectionView *feedView;
@property (strong, nonatomic) NSMutableArray *feedDataArray;

@end

@implementation FeedViewController

@synthesize feedView;
@synthesize feedDataArray;

- (void) viewDidLoad
{
    feedDataArray = [[NSMutableArray alloc] init];
    [self setupTestImages];
}

- (void)viewDidLayoutSubviews
{
    feedView = [[UICollectionView alloc] initWithFrame:self.view.bounds collectionViewLayout:[[UICollectionViewFlowLayout alloc] init]];
    [feedView registerClass:[PhotoCollectionViewCell class] forCellWithReuseIdentifier:kPhotoCellIdentifier];
    [feedView setBackgroundColor:[UIColor whiteColor]];
    [feedView setDelegate:self];
    [feedView setDataSource:self];
    [self.view addSubview:feedView];
    [feedView reloadData];
    
    self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithBarButtonSystemItem:UIBarButtonSystemItemAdd target:self action:@selector(addItem)];
}

- (void) setupTestImages
{
    [feedDataArray addObject:[UIImage imageNamed:@"drunk1.jpg"]];
    [feedDataArray addObject:[UIImage imageNamed:@"drunk2.jpg"]];
    [feedDataArray addObject:[UIImage imageNamed:@"drunk3.jpg"]];
}

- (void) addItem
{
    [self.navigationController pushViewController:[[DrawingViewController alloc] init]
	    animated:YES];
}

#pragma mark - <UICollectionViewDatasource>

- (NSInteger)collectionView:(UICollectionView *)view numberOfItemsInSection:(NSInteger)section;
{
    return [feedDataArray count];
}

- (NSInteger)numberOfSectionsInCollectionView:(UICollectionView *)collectionView
{
    return 1;
}

- (UICollectionViewCell *)collectionView:(UICollectionView *)cv cellForItemAtIndexPath:(NSIndexPath *)indexPath;
{
    PhotoCollectionViewCell *cell = [cv dequeueReusableCellWithReuseIdentifier:kPhotoCellIdentifier forIndexPath:indexPath];
    [cell setPhoto:[feedDataArray objectAtIndex:indexPath.row]];
    
    return cell;
}

#pragma mark - <UICollectionViewFlowLayoutDelegate>

- (void)collectionView:(UICollectionView *)collectionView didSelectItemAtIndexPath:(NSIndexPath *)indexPath
{
    return;
}

- (CGSize)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout*)collectionViewLayout sizeForItemAtIndexPath:(NSIndexPath *)indexPath
{
    CGFloat squareSideSize = [[UIScreen mainScreen] bounds].size.width - [self collectionView:nil layout:nil insetForSectionAtIndex:nil].left - [self collectionView:nil layout:nil insetForSectionAtIndex:nil].right;
    return CGSizeMake(squareSideSize, squareSideSize);
}

- (UIEdgeInsets)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout*)collectionViewLayout insetForSectionAtIndex:(NSInteger)section
{
    return UIEdgeInsetsMake(10,10,10,10);
}

- (CGFloat)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout*)collectionViewLayout minimumLineSpacingForSectionAtIndex:(NSInteger)section
{
    return 10.f;
}

@end
