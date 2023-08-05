# import copy
# import math
# import re

from datetime import date, datetime, timedelta
# from operator import itemgetter

import facebook
import time
import traceback
# import dateutil.parser

# from utils.common import date_formatter
# from utils.common.custom_exceptions import CustomException, ClassifiedException, FacebookGraphAPIError
# from utils.common.convert_list import split_list

class CustomException(Exception):
    #생성할때 value 값을 입력 받는다.
    def __init__(self, value):
        self.value = value

    #생성할때 받은 value 값을 확인 한다.
    def __str__(self):
        return self.value

# #Exception 클래스를 상속한 클래스를 만든다 (분류된 Exception에 사용)
class ClassifiedException(Exception):
    # 생성할때 value 값을 입력 받는다.
    def __init__(self, value):
        self.value = value

    # 생성할때 받은 value 값을 확인 한다.
    def __str__(self):
        return self.value
#
# class FacebookGraphAPIError(Exception):
#     # 생성할때 value 값을 입력 받는다.
#     def __init__(self, value):
#         self.value = value
#
#     # 생성할때 받은 value 값을 확인 한다.
#     def __str__(self):
#         return self.value

class Instagram:
    INSTAGRAM_BUSINESS_ACCOUNTS_FIELDS = "instagram_business_account{id,ig_id,username,biography,followers_count,follows_count,media_count,name,website,profile_picture_url,media.limit(1)},tasks,access_token,category"
    INSTAGRAM_BUSINESS_ACCOUNT_FIELDS = "id,ig_id,username,biography,followers_count,follows_count,media_count,name,website,profile_picture_url"
    INSTAGRAM_BUSINESS_ACCOUNT_DISCOVERY_FIELDS = "id,ig_id,username,biography,followers_count,follows_count,media_count,website,name,profile_picture_url"
    INSTAGRAM_BUSINESS_ACCOUNT_CHECK_MEDIA_DISCOVERY_FIELDS = "id"
    INSTAGRAM_BUSINESS_ACCOUNT_MEDIA_DISCOVERY_FIELDS = "id,caption,comments_count,like_count,media_url,media_type,owner,timestamp,permalink"
    INSTAGRAM_BUSINESS_ACCOUNT_INSIGHT_LIFETIME = "audience_gender_age,audience_locale,audience_country,audience_city,online_followers"
    INSTAGRAM_BUSINESS_ACCOUNT_INSIGHT_DAY = "email_contacts,get_directions_clicks,impressions,phone_call_clicks,profile_views,reach,text_message_clicks,website_clicks,follower_count"
    COMMENTS_FIELDS = "id,username,text,like_count,timestamp"
    COMMENTS_REPLIES_FIELDS = COMMENTS_FIELDS + ",replies.limit(50){" + COMMENTS_FIELDS + "}"
    MEDIA_FIELDS = "id,ig_id,username,is_comment_enabled,media_type,media_url,permalink,shortcode,thumbnail_url,caption,owner,comments{" + COMMENTS_REPLIES_FIELDS + "},comments_count,like_count,timestamp"
    MEDIA_SUMMARY_FIELDS = "id,media_type,like_count,comments_count,media_url,thumbnail_url,timestamp"
    MEDIA_COLLECT_FIELDS = "id,ig_id,caption,shortcode,permalink,username,timestamp,media_url,owner,media_type,thumbnail_url,like_count,comments_count"
    BEST_MEDIA_FIELDS = "id,permalink,media_type,media_url,thumbnail_url,comments_count,like_count,timestamp"
    LIKE_COMMENT_FIELDS = "ig_id,like_count,comments_count,comments"
    TAGS_FIELDS = "id,caption,comments_count,like_count,media_url,media_type,owner,comments"
    # MENTIONED_MEDIA_FIELDS = "caption, comments, comments_count, like_count, media_type, media_url, owner"
    # MENTIONED_COMMENT_FIELDS = "id, like_count, media, text, timestamp, user"
    MENTIONED_MEDIA_FIELDS = "caption, comments_count, like_count, media_type, media_url, owner"
    MENTIONED_COMMENT_FIELDS = "id, like_count, media, text, timestamp, user"
    PHOTO_METRICS = "engagement,impressions,reach,saved"
    VIDEO_METRICS = "engagement,impressions,reach,saved,video_views"
    CAROUSEL_METRICS = "carousel_album_engagement,carousel_album_impressions,carousel_album_reach,carousel_album_saved,carousel_album_video_views"
    STORY_METRICS = "exits,impressions,reach,replies,taps_forward,taps_back"
    FOLLOWERS_INSIGHTS_METRICS = "follower_count"
    ONLINE_FOLLOWERS_METRICS = "online_followers"
    APP_PERMISSIONS = "permissions"

    def __init__(self, version='v7.0', fb_access_token=None, limit=9):
        self.facebook_sdk_version = version
        self.graph = facebook.GraphAPI(access_token=fb_access_token, version=self.facebook_sdk_version)
        self.limit = limit

    def init_params(self):
        if self.limit:
            params = {
                'limit': self.limit
            }
        else:
            params = {}

        return params

    def get_all_request(self, url, params, data_key="data"):
        '''
        Facebook Graph API 페이징 전체 가져오기
        '''
        ret = []
        try:
            while True:
                result = self.graph.request(url, args=params)
                data = result[data_key]
                ret += data

                if 'paging' in result:
                    paging = result["paging"]
                    if len(data) < 1:
                        break

                    if 'next' in paging:
                        cursors = paging['cursors']
                        after = cursors['after']
                        params['after'] = after
                    else:
                        break
                else:
                    break
        except Exception as e:
            print(e)
            raise CustomException("서버 통신 에러 입니다.")
        return ret

    def get_period_request(self, url, params, date_from, date_to, data_key="data"):
        '''
        특정 기간에 포함된 Paging 가져오기
        '''
        ret = []
        try:
            print("get_period_request", date_from, date_to)
            if date_to is None:
                date_to = datetime.now()

            end_loop = False
            while True:
                result = self.graph.request(url, args=params)
                data = result[data_key]
                for item in data:
                    item_date = datetime.strptime(item['timestamp'], '%Y-%m-%dT%H:%M:%S+0000')
                    if date_from < item_date and date_to > item_date:
                        ret.append(item)
                    else:
                        # 벗어나는 기간일때,
                        # 최소한 date_from 기간보다 큰 경우까지는 체크 해야한다.
                        if date_from < item_date:
                            continue
                        else:
                            print("마지막 체크 시간", item['timestamp'])
                            end_loop = True
                            break
                if end_loop:
                    break

                if 'paging' in result:
                    paging = result["paging"]
                    if len(data) < 1:
                        break

                    if 'next' in paging:
                        cursors = paging['cursors']
                        after = cursors['after']
                        params['after'] = after
                    else:
                        break
                else:
                    break
        except Exception as e:
            raise CustomException("서버 통신 에러 입니다.")
        return ret

    def get_instagram_business_accounts(self):
        '''
        권한이 있는 인스타그램 계정 리스트 가져오기
        '''
        ig_accounts = []
        try:
            params = self.init_params()
            params["fields"] = self.INSTAGRAM_BUSINESS_ACCOUNTS_FIELDS
            params["locale"] = 'ko_kr'
            params["limit"] = 50
            accounts = self.get_all_request("me/accounts", params)

            for account in accounts:
                if "instagram_business_account" in account:
                    instagram_business_account = account["instagram_business_account"]
                    tasks = None
                    if "tasks" in account:
                        tasks = account["tasks"]
                    instagram_business_account["page_id"] = account["id"]
                    instagram_business_account["perms"] = tasks
                    instagram_business_account["page_access_token"] = account["access_token"]
                    instagram_business_account["category"] = account.get('category', None)
                    ig_accounts.append(instagram_business_account)
        except Exception as e:
            print(traceback.format_exc())
            raise CustomException('인스타그램 계정 리스트를 가져오는데 실패했습니다.')
        ig_accounts = sorted(ig_accounts, key=lambda k: k['username'])
        return ig_accounts

    def get_instagram_business_account(self, instagram_business_account_id):
        '''
        인스타그램 계정 정보 가져오기
        '''
        ig_account = {}
        try:
            params = self.init_params()
            params["fields"] = self.INSTAGRAM_BUSINESS_ACCOUNT_FIELDS
            ig_account = self.graph.request(instagram_business_account_id, args=params)
        except Exception as e:
            raise CustomException('인스타그램 계정을 가져오는데 실패했습니다.')
        return ig_account

    # def get_instagram_business_account_discovery(self, instagram_business_account_id, username):
    #     '''
    #     다른 인스타그램 비즈니스 계정 정보 가져오기
    #     '''
    #     try:
    #         params = self.init_params()
    #         # 요청 파라미터
    #         params['fields'] = 'business_discovery.username(' + username + ')' \
    #                                                                        '{' + self.INSTAGRAM_BUSINESS_ACCOUNT_DISCOVERY_FIELDS + '}'
    #         # 데이터 요청
    #         ig_account = self.graph.request(instagram_business_account_id, args=params)
    #     except facebook.GraphAPIError as e:
    #         error = e.result['error']
    #         code = error['code']
    #         error_subcode = error.get('error_subcode')
    #
    #         # 계정명이 잘못되었거나 비즈니스 계정이 아닐 경우 - 경쟁사 data 삭제
    #         if code == 110 and error_subcode == 2207013:
    #             from ig_compete_account.models import IgCompeteAccount
    #             from ig_account_competitor.models import IgAccountCompetitor
    #             from ig_compete_account_hashtag.models import IgCompeteAccountHashtag
    #
    #             try:
    #                 ig_compete_account = IgCompeteAccount.objects.get(username=username)
    #                 # ig_account_competitor delete
    #                 IgAccountCompetitor.objects.filter(ig_competitor_account_id=ig_compete_account.id).delete()
    #                 # ig_compete_account_hashtag delete
    #                 IgCompeteAccountHashtag.objects.filter(ig_competitor_account_id=ig_compete_account.id).delete()
    #                 # ig_compete_account delete
    #                 ig_compete_account.delete()
    #             except IgCompeteAccount.DoesNotExist:
    #                 pass
    #             except Exception as e:
    #                 raise ClassifiedException('인스타그램 계정명이 잘못되었거나 비즈니스 계정이 아닙니다.')
    #
    #         raise ClassifiedException('인스타그램 계정명이 잘못되었거나 비즈니스 계정이 아닙니다.')
    #     except Exception as e:
    #         raise ClassifiedException('인스타그램 계정명이 잘못되었거나 비즈니스 계정이 아닙니다.')
    #     return ig_account

    def get_instagram_business_account_media_discovery(self, instagram_business_account_id, username, after=None,
                                                       is_check_id=False):
        '''
        다른 인스타그램 비즈니스 계정의 전체 미디어 리스트 가져오기
        '''
        try:
            params = self.init_params()

            fields = 'business_discovery.username(' + username + ')'
            if after:
                fields += '{media.after(' + after + '){'
            else:
                fields += '{media{'

            if is_check_id:
                fields += self.INSTAGRAM_BUSINESS_ACCOUNT_CHECK_MEDIA_DISCOVERY_FIELDS
            else:
                fields += self.INSTAGRAM_BUSINESS_ACCOUNT_MEDIA_DISCOVERY_FIELDS

            fields += '}}'

            params['fields'] = fields

            # print('get_instagram_business_account_media_discovery')
            # print(params)

            try:
                res = self.graph.request(instagram_business_account_id, args=params)
            except Exception as e:
                try:
                    time.sleep(3)
                    res = self.graph.request(instagram_business_account_id, args=params)
                except Exception as e:
                    try:
                        time.sleep(3)
                        res = self.graph.request(instagram_business_account_id, args=params)
                    except Exception as e:
                        try:
                            time.sleep(3)
                            res = self.graph.request(instagram_business_account_id, args=params)
                        except Exception as e:
                            time.sleep(3)
                            res = self.graph.request(instagram_business_account_id, args=params)

            media = res['business_discovery'].get('media')

            if media:
                if media.get('paging'):
                    if 'after' in res['business_discovery']['media']['paging']['cursors']:
                        media['is_next_page'] = True
                    else:
                        media['is_next_page'] = False
                else:
                    media['paging'] = {}
                    media['is_next_page'] = False
            else:
                media = {
                    'data': [],
                    'paging': {},
                    'is_next_page': False
                }

        except Exception as e:
            raise CustomException('인스타그램 비즈니스 계정 미디어정보를 가져오는데 실패했습니다.')
        return media

    def get_instagram_business_account_all_media_discovery(self, instagram_business_account_id, username):
        '''
        다른 인스타그램 비즈니스 계정의 전체 미디어 리스트 가져오기
        '''
        try:
            params = self.init_params()
            params['fields'] = 'business_discovery.username(' + username + ')' \
                                                                           '{' + self.INSTAGRAM_BUSINESS_ACCOUNT_DISCOVERY_FIELDS + ',' \
                                                                                                                                    'media{' + self.INSTAGRAM_BUSINESS_ACCOUNT_MEDIA_DISCOVERY_FIELDS + '}}'
            res = self.graph.request(instagram_business_account_id, args=params)

            obj = {
                'id': res['business_discovery']['id'],
                'ig_id': res['business_discovery']['ig_id'],
                'username': res['business_discovery']['username'],
                'biography': res['business_discovery'].get('biography', None),
                'followers_count': res['business_discovery']['followers_count'],
                'follows_count': res['business_discovery']['follows_count'],
                'media_count': res['business_discovery']['media_count'],
                'website': res['business_discovery'].get('website', None),
                'name': res['business_discovery']['name'],
                'profile_picture_url': res['business_discovery']['profile_picture_url'],
                'medias': res['business_discovery']['media']['data']
            }

            # 다음 페이지
            if 'paging' in res['business_discovery']['media']:
                cursors = res['business_discovery']['media']['paging']['cursors']
                while True:
                    if 'after' in cursors:
                        params['fields'] = 'business_discovery.username(' + username + ')' \
                                                                                       '{media.after(' + cursors[
                                               'after'] + ')' \
                                                          '{' + self.INSTAGRAM_BUSINESS_ACCOUNT_MEDIA_DISCOVERY_FIELDS + '}}'
                        after_medias = self.graph.request(instagram_business_account_id, args=params)
                        if 'media' in after_medias['business_discovery']:
                            obj['medias'] += after_medias['business_discovery']['media']['data']
                            cursors = after_medias['business_discovery']['media']['paging']['cursors']
                        else:
                            break
                    else:
                        # after 가 없을 경우 while 문 종료
                        break
        except Exception as e:
            raise CustomException('인스타그램 비즈니스 계정 미디어정보를 가져오는데 실패했습니다.')
        return obj

    def get_media_paging(self, instagram_business_account_id, fields=MEDIA_FIELDS, after=None, limit=25):
        params = self.init_params()
        params['limit'] = limit
        if after:
            params['after'] = after

        params["fields"] = fields
        try:
            media = self.graph.request(instagram_business_account_id + "/media", args=params)
        except Exception as e:
            try:
                time.sleep(3)
                media = self.graph.request(instagram_business_account_id + "/media", args=params)
            except Exception as e:
                try:
                    time.sleep(3)
                    media = self.graph.request(instagram_business_account_id + "/media", args=params)
                except Exception as e:
                    try:
                        time.sleep(3)
                        media = self.graph.request(instagram_business_account_id + "/media", args=params)
                    except Exception as e:
                        try:
                            time.sleep(3)
                            media = self.graph.request(instagram_business_account_id + "/media", args=params)
                        except Exception as e:
                            raise CustomException('인스타그램 미디어를 가져오는데 실패했습니다.')
        media['data'] = media['data'] if 'data' in media else []
        if 'paging' in media:
            if 'after' in media['paging']['cursors']:
                media['is_next_page'] = True
            else:
                media['is_next_page'] = False
        else:
            media['paging'] = {}
            media['is_next_page'] = False

        return media

    # def get_media_list_for_ids(self, instagram_business_account_id, selected_media_ids, fields=MEDIA_FIELDS,
    #                            instagram_business_account_at=None):
    #     '''
    #     인스타그램 계정의 미디어 리스트 가져오기
    #     '''
    #     media = {}
    #     try:
    #         media_ids = []
    #         saved_media_ids = []
    #         media_list = []
    #
    #         for selected_media_id in selected_media_ids:
    #             params = self.init_params()
    #             params["fields"] = fields
    #             try:
    #                 media_obj = self.graph.request(selected_media_id, args=params)
    #                 media_list.append(media_obj)
    #             except facebook.GraphAPIError as e:
    #                 error = e.result['error']
    #                 if error['code'] == 100 and error['error_subcode'] == 33:
    #                     IgMedia.objects.filter(media_id=selected_media_id).update(is_deleted=True)
    #
    #         media["data"] = media_list
    #
    #         for (index, media_data) in enumerate(media['data']):
    #             media_ids.append(media_data['id'])
    #
    #         if instagram_business_account_at != None:
    #             instagram_business_account_at_str = date_formatter.datetime_to_formatted_YYYY_MM_DD_HH_MM_SS(
    #                 instagram_business_account_at)
    #
    #             for (index, media_data) in enumerate(media['data']):
    #                 media_timestamp = media_data['timestamp']
    #                 datetime_media_timestamp_str = date_formatter.datetime_to_formatted_YYYY_MM_DD_HH_MM_SS(
    #                     dateutil.parser.parse(media_timestamp))
    #
    #                 datediff_min = date_formatter.datediff_min(instagram_business_account_at_str,
    #                                                            datetime_media_timestamp_str, "%Y-%m-%d %H:%M:%S")
    #                 # print(datediff_min)
    #                 if datediff_min > 0:
    #                     saved_media_ids.append(media_data['id'])
    #
    #             # saved 값 구하기 위한 큰 요청
    #             if saved_media_ids != []:
    #                 medias_insight = self.get_media_type_insights(saved_media_ids)
    #                 for (index, media_id) in enumerate(medias_insight):
    #                     saved = medias_insight[media_id]['data'][3]['values'][0]['value']
    #                     media['data'][index]['saved'] = saved
    #
    #         media['data'] = media['data'] if 'data' in media else []
    #         media['paging'] = media['paging'] if 'paging' in media else {}
    #
    #     except FacebookGraphAPIError as fe:
    #         raise FacebookGraphAPIError(fe)
    #     except Exception as e:
    #         raise CustomException('인스타그램 미디어를 가져오는데 실패했습니다.')
    #     return media

    # def get_media_list(self, instagram_business_account_id, fields=MEDIA_FIELDS, after=None,
    #                    instagram_business_account_at=None):
    #     '''
    #     인스타그램 계정의 미디어 리스트 가져오기
    #     '''
    #     media = {}
    #     try:
    #
    #         # print("get_media_list")
    #         # print(instagram_business_account_at)
    #         params = self.init_params()
    #         if after:
    #             params['after'] = after
    #         params["fields"] = fields
    #         media = self.graph.request(instagram_business_account_id + "/media", args=params)
    #
    #         media_ids = []
    #         saved_media_ids = []
    #
    #         for (index, media_data) in enumerate(media['data']):
    #             media_ids.append(media_data['id'])
    #
    #         if instagram_business_account_at != None:
    #             instagram_business_account_at_str = date_formatter.datetime_to_formatted_YYYY_MM_DD_HH_MM_SS(
    #                 instagram_business_account_at)
    #
    #             for (index, media_data) in enumerate(media['data']):
    #                 media_timestamp = media_data['timestamp']
    #                 datetime_media_timestamp_str = date_formatter.datetime_to_formatted_YYYY_MM_DD_HH_MM_SS(
    #                     dateutil.parser.parse(media_timestamp))
    #
    #                 datediff_min = date_formatter.datediff_min(instagram_business_account_at_str,
    #                                                            datetime_media_timestamp_str, "%Y-%m-%d %H:%M:%S")
    #                 # print(datediff_min)
    #                 if datediff_min > 0:
    #                     saved_media_ids.append(media_data['id'])
    #
    #             # saved 값 구하기 위한 큰 요청
    #             if saved_media_ids != []:
    #                 medias_insight = self.get_media_type_insights(saved_media_ids)
    #                 for (index, media_id) in enumerate(medias_insight):
    #                     saved = medias_insight[media_id]['data'][3]['values'][0]['value']
    #                     media['data'][index]['saved'] = saved
    #
    #         media['data'] = media['data'] if 'data' in media else []
    #         media['paging'] = media['paging'] if 'paging' in media else {}
    #     except facebook.GraphAPIError as e:
    #         error = e.result['error']
    #         code = error['code']
    #         message = error['message']
    #         if 'permission' in message:
    #             raise FacebookGraphAPIError('페이스북 페이지 접근 권한이 수정되어 데이터 확인이 불가합니다./n페이스북 비즈니스 관리자에서 회원님의 접근권한을 확인해 주세요./n문의사항은 help@bigcial.com으로 연락 바랍니다.')
    #         else:
    #             raise
    #     except Exception as e:
    #         raise CustomException('인스타그램 미디어를 가져오는데 실패했습니다.')
    #     return media
    #
    # def get_all_media_list(self, instagram_business_account_id):
    #     '''
    #     인스타그램 계정의 미디어 전체 리스트 가져오기
    #     '''
    #     try:
    #         params = self.init_params()
    #         params['fields'] = self.MEDIA_FIELDS
    #         media = self.get_all_request(instagram_business_account_id + '/media', params)
    #     except Exception as e:
    #         raise CustomException('인스타그램 미디어를 가져오는데 실패했습니다.')
    #
    #     return media
    #
    # def get_best_media(self, instagram_business_account_id, day, count):
    #     '''
    #     최근 day 일, 베스트 미디어 가져오기 (좋아요, 댓글 기준)
    #     '''
    #     params = self.init_params()
    #     params['fields'] = self.MEDIA_FIELDS
    #
    #     date_to = datetime.now()
    #     date_from = date_to - timedelta(days=day)
    #
    #     media_list = self.get_period_request(instagram_business_account_id + '/media', params, date_from, date_to)
    #
    #     # 베스트 미디어 count 개수 만큼 자르기
    #     best_like_medias = sorted(media_list, key=lambda bm: bm['like_count'], reverse=True)[:count]
    #     best_comments_medias = sorted(media_list, key=lambda bm: bm['comments_count'], reverse=True)[:count]
    #
    #     result = {
    #         'best_comments_medias': best_comments_medias,
    #         'best_like_medias': best_like_medias
    #     }
    #
    #     return result
    #
    # def get_best_medias(self, instagram_business_account_id, day, count):
    #     '''
    #     메인페이지 포스트 TOP5 평균, 베스트게시글 가져오기
    #     '''
    #     try:
    #         params = self.init_params()
    #         params['fields'] = self.BEST_MEDIA_FIELDS
    #
    #         # 최근 day일
    #         date_to = datetime.now()
    #         date_from = date_to - timedelta(days=day)
    #
    #         print(date_to)
    #         print(date_from)
    #
    #         # 비교기간
    #         compare_date_to = date_from - timedelta(days=1)
    #         compare_date_from = compare_date_to - timedelta(days=day)
    #         print(compare_date_to)
    #         print(compare_date_from)
    #
    #         # 기간내 미디어 목록
    #         medias = self.get_period_request(instagram_business_account_id + '/media', params, date_from, date_to)
    #         compare_medias = self.get_period_request(instagram_business_account_id + '/media', params,
    #                                                  compare_date_from, compare_date_to)
    #
    #         # 베스트 미디어 count 만큼 자르기 (like 개수 기준)
    #         best_medias = sorted(medias, key=lambda media: media['like_count'], reverse=True)[:count]
    #         compare_best_medias = sorted(compare_medias, key=lambda compare_media: compare_media['like_count'],
    #                                      reverse=True)[:count]
    #
    #         # save 데이터 설정
    #         best_medias = self.set_media_saved_count(best_medias)
    #         compare_best_medias = self.set_media_saved_count(compare_best_medias)
    #
    #         if len(best_medias) > 0:
    #             avg_like = self.sum_item(best_medias, 'like_count')
    #             avg_comments = self.sum_item(best_medias, 'comments_count')
    #             avg_saved = self.sum_item(best_medias, 'saved')
    #
    #             if len(compare_best_medias) > 0:
    #                 avg_compare_like = self.sum_item(compare_best_medias, 'like_count')
    #                 avg_compare_comments = self.sum_item(compare_best_medias, 'comments_count')
    #                 avg_compare_saved = self.sum_item(compare_best_medias, 'saved')
    #
    #                 diff_best_like_avg = avg_like - avg_compare_like
    #                 diff_best_comments_avg = avg_comments - avg_compare_comments
    #                 diff_best_saved_avg = avg_saved - avg_compare_saved
    #             else:
    #                 diff_best_like_avg = 0
    #                 diff_best_comments_avg = 0
    #                 diff_best_saved_avg = 0
    #         else:
    #             avg_like = 0
    #             avg_comments = 0
    #             avg_saved = 0
    #             diff_best_like_avg = 0
    #             diff_best_comments_avg = 0
    #             diff_best_saved_avg = 0
    #
    #         result = {
    #             'best_media': best_medias,
    #             'best_like_avg': avg_like,
    #             'best_comments_avg': avg_comments,
    #             'best_saved_avg': avg_saved,
    #             'diff_best_like_avg': diff_best_like_avg,
    #             'diff_best_comments_avg': diff_best_comments_avg,
    #             'diff_best_saved_avg': diff_best_saved_avg,
    #         }
    #     except Exception as e:
    #         raise CustomException('메인페이지 포스트 TOP5를 가져오는데 실패했습니다.')
    #     return result
    #
    # def set_media_saved_count(self, media_list):
    #     media_ids = []
    #     for index, media in enumerate(media_list):
    #         media_ids.append(media_list[index]['id'])
    #
    #     # saved 값 구하기 위한 큰 요청
    #     medias_insight = self.get_media_type_insights(media_ids)
    #     if medias_insight is None:
    #         return {}
    #
    #     for index, media_id in enumerate(medias_insight):
    #         saved = medias_insight[media_id]['data'][3]['values'][0]['value']
    #         media_list[index]['saved'] = saved
    #     return media_list
    #
    # def create_creation_id(self, instagram_business_account_id, params):
    #     creation_id = self.graph.request(instagram_business_account_id + '/media', post_args=params, method='POST')
    #     return creation_id
    #
    # def media_publish(self, instagram_business_account_id, params):
    #     media = self.graph.request(instagram_business_account_id + '/media_publish', post_args=params, method='POST')
    #     return media
    #
    # # def set_summary_media_for_media_ids(self, instagram_business_account_id, media_ids,summary_medias):
    # #
    #
    #
    # def set_summary_medias(self, instagram_business_account_id, since_timestamp, until_timestamp, summary_medias,
    #                        after):
    #     try:
    #         # 재귀함수 탈출 조건
    #         to_exit = False
    #
    #         # 페이징 처리 - 호출은 최소한으로 1번만.
    #         media_list = self.get_media_list(instagram_business_account_id, self.MEDIA_SUMMARY_FIELDS, after)
    #         medias = media_list['data']
    #         if medias != []:
    #             after = media_list['paging']['cursors']['after']
    #
    #             # 페이징 처리해서 가져온 미디어들중 기간안에 해당하는 미디어
    #             for media in medias:
    #                 media_timestamp = time.mktime(
    #                     datetime.strptime(media['timestamp'], '%Y-%m-%dT%H:%M:%S+0000').timetuple())
    #
    #                 if since_timestamp <= media_timestamp <= until_timestamp:
    #                     media['timestamp'] = date_formatter.datetime_to_formatted_GMT_YYYY_MM_DD_HH_MM_SS(dateutil.parser.parse(media['timestamp']))
    #                     summary_medias.append(media)
    #
    #                 if media_timestamp < since_timestamp:
    #                     to_exit = True
    #                     break
    #         else:
    #             to_exit = True
    #
    #         if to_exit:
    #             return summary_medias
    #         else:
    #             return self.set_summary_medias(instagram_business_account_id, since_timestamp, until_timestamp,
    #                                         summary_medias, after)
    #     except FacebookGraphAPIError as fe:
    #         raise FacebookGraphAPIError(str(fe))
    #     except Exception as e:
    #         raise
    #
    # def get_media_summary_for_media_ids(self, instagram_business_account_id, ig_account_media,
    #                                     instagram_business_account_at):
    #     '''
    #     특정 기간 미디어 요약
    #     '''
    #     # 기간
    #     # summary_medias = []
    #     # summary_medias = self.set_summary_media_for_media_ids(instagram_business_account_id, media_ids,summary_medias)
    #
    #     # 요약
    #     best_media_id = None
    #     summary_media_ids = []
    #     summary = {
    #         'media_count': len(ig_account_media),
    #         'like_count': 0,
    #         'comments_count': 0,
    #         'saved': 0,
    #         'best_media': None,
    #         'medias': ig_account_media
    #     }
    #
    #     saved_media_ids = []
    #
    #     temp_like_count = 0
    #     for summary_media in ig_account_media:
    #         summary_media_ids.append(summary_media['media_id'])
    #
    #         media_at = summary_media['media_at']
    #         if date_formatter.datediff_min(str(instagram_business_account_at), str(media_at),
    #                                        "%Y-%m-%d %H:%M:%S") > 0:
    #             saved_media_ids.append(summary_media['media_id'])
    #
    #         # 기간안의 베스트 미디어
    #         if summary_media['like_count'] > temp_like_count:
    #             best_media_id = summary_media['media_id']
    #             temp_like_count = summary_media['like_count']
    #
    #         summary['like_count'] += summary_media['like_count']
    #         summary['comments_count'] += summary_media['comment_count']
    #
    #     # # saved 값 구하기 위한 큰 요청
    #     if len(saved_media_ids) > 0:
    #         split_ids_list = split_list(saved_media_ids)
    #         for split_ids in split_ids_list:
    #             summary_medias_insight = self.get_media_type_insights(split_ids)
    #
    #             for (index, summary_media_id) in enumerate(summary_medias_insight):
    #                 summary_media_saved = summary_medias_insight[summary_media_id]['data'][3]['values'][0]['value']
    #                 summary['medias'][index]['saved'] = summary_media_saved
    #                 summary['saved'] += summary_media_saved
    #
    #         if best_media_id in saved_media_ids:
    #             summary['best_media'] = self.get_media_detail(best_media_id, is_save_able=True)
    #             summary['best_media']['saved'] = \
    #             self.get_media_type_insights(best_media_id)[best_media_id]['data'][3]['values'][0]['value']
    #         else:
    #             summary['best_media'] = self.get_media_detail(best_media_id, is_save_able=False)
    #     return summary
    #
    # def get_media_summary(self, instagram_business_account_id, since, until, instagram_business_account_at,
    #                       selected_media_ids=None):
    #     '''
    #     특정 기간 미디어 요약
    #     '''
    #     try:
    #
    #         # 기간
    #         since_timestamp = time.mktime(datetime.strptime(since, '%Y%m%d').timetuple())
    #         until_timestamp = time.mktime((datetime.strptime(until, '%Y%m%d') + timedelta(1)).timetuple())
    #
    #         summary_medias = []
    #         summary_medias = self.set_summary_medias(instagram_business_account_id, since_timestamp, until_timestamp,
    #                                                 summary_medias, None)
    #         # print('summary_medias : ', summary_medias)
    #
    #         if selected_media_ids == None:
    #             pass
    #         else:
    #             temp_media = []
    #             for summary_media in summary_medias:
    #                 if summary_media.get('id') in selected_media_ids:
    #                     temp_media.append(summary_media)
    #             summary_medias = temp_media
    #
    #         # 요약
    #         best_media_id = None
    #         summary_media_ids = []
    #         summary = {
    #             'media_count': len(summary_medias),
    #             'like_count': 0,
    #             'comments_count': 0,
    #             'saved': 0,
    #             'best_media': None,
    #             'medias': summary_medias
    #         }
    #
    #         saved_media_ids = []
    #
    #         temp_like_count = -1
    #         for summary_media in summary_medias:
    #             summary_media_ids.append(summary_media['id'])
    #
    #             media_timestamp = summary_media['timestamp']
    #             datetime_media_timestamp_str = date_formatter.datetime_to_formatted_YYYY_MM_DD_HH_MM_SS(
    #                 dateutil.parser.parse(media_timestamp))
    #
    #             if instagram_business_account_at:
    #                 instagram_business_account_at_str = date_formatter.datetime_to_formatted_YYYY_MM_DD_HH_MM_SS(
    #                     instagram_business_account_at)
    #                 if date_formatter.datediff_min(instagram_business_account_at_str, datetime_media_timestamp_str,
    #                                             "%Y-%m-%d %H:%M:%S") > 0:
    #                     saved_media_ids.append(summary_media['id'])
    #
    #             # 기간안의 베스트 미디어
    #             if summary_media['like_count'] > temp_like_count:
    #                 best_media_id = summary_media['id']
    #                 temp_like_count = summary_media['like_count']
    #
    #             summary['like_count'] += summary_media['like_count']
    #             summary['comments_count'] += summary_media['comments_count']
    #
    #         # saved 값 구하기 위한 큰 요청
    #         if len(saved_media_ids) > 0:
    #             split_num = 50
    #             split_ids_list = split_list(saved_media_ids, split_num)
    #             for idx, split_ids in enumerate(split_ids_list):
    #                 summary_medias_insight = self.get_media_type_insights(split_ids)
    #
    #                 for (index, summary_media_id) in enumerate(summary_medias_insight):
    #                     summary_media_saved = summary_medias_insight[summary_media_id]['data'][3]['values'][0]['value']
    #                     medias_index = idx*split_num + index
    #                     summary['medias'][medias_index]['saved'] = summary_media_saved
    #                     summary['saved'] += summary_media_saved
    #
    #             if best_media_id in saved_media_ids:
    #                 summary['best_media'] = self.get_media_detail(best_media_id, is_save_able=True)
    #                 summary['best_media']['saved'] = \
    #                 self.get_media_type_insights(best_media_id)[best_media_id]['data'][3]['values'][0]['value']
    #             else:
    #                 summary['best_media'] = self.get_media_detail(best_media_id, is_save_able=False)
    #         return summary
    #     except FacebookGraphAPIError as fe:
    #         raise FacebookGraphAPIError(str(fe))
    #     except Exception as e:
    #         raise
    #
    # def sum_item(self, data, key):
    #     total = 0
    #     try:
    #         for item in data:
    #             total += item[key]
    #     except Exception as e:
    #         print(traceback.format_exc())
    #         total = 0
    #     return int(total / len(data))
    #
    # def get_media_comment_list(self, media_id, after=None, fields=COMMENTS_REPLIES_FIELDS):
    #     '''
    #     미디어의 댓글 목록 가져오기
    #     '''
    #     comments = {}
    #     try:
    #         params = self.init_params()
    #         if after:
    #             params['after'] = after
    #         params["fields"] = fields
    #
    #         comments = self.graph.request(media_id + "/comments", args=params)
    #         comments['data'] = comments['data'] if 'data' in comments else []
    #         comments['paging'] = comments['paging'] if 'paging' in comments else {}
    #
    #         # 댓글의 댓글 data set
    #         # 댓글 최신순
    #         comments['data'] = sorted(comments['data'], key=lambda k: k['timestamp'], reverse=True)
    #         for comment in comments['data']:
    #             if 'replies' in comment:
    #                 replies = comment.get('replies')
    #                 if 'paging' in replies:
    #                     params = self.init_params()
    #                     params["fields"] = self.COMMENTS_FIELDS
    #                     replies = self.get_all_request(comment.get('id') + '/replies', params)
    #                 else:
    #                     replies = replies.get('data')
    #
    #                 # 대댓글 최초 등록순으로
    #                 replies = sorted(replies, key=lambda k: k['timestamp'])
    #                 for reply in replies:
    #                     reply['timestamp'] = date_formatter.datetime_to_formatted_GMT_YYYY_MM_DD_HH_MM_SS(dateutil.parser.parse(reply['timestamp']))
    #                 comment['replies'] = replies
    #             else:
    #                 comment['replies'] = None
    #     except Exception as e:
    #         print(traceback.format_exc())
    #         raise CustomException('인스타그램 댓글을 가져오는데 실패했습니다.')
    #     return comments
    #
    # def get_all_media_comment_list(self, media_id):
    #     '''
    #     미디어의 전체 댓글 목록 가져오기
    #     '''
    #     comments = {}
    #     try:
    #         params = self.init_params()
    #         params["fields"] = self.COMMENTS_REPLIES_FIELDS
    #         comments = self.get_all_request(media_id + "/comments", params)
    #         # print(comments)
    #
    #         # 댓글의 댓글 data set
    #         # 댓글 최신순
    #         comments = sorted(comments, key=lambda k: k['timestamp'], reverse=True)
    #         for comment in comments:
    #             if 'replies' in comment:
    #                 replies = comment.get('replies')
    #                 if 'paging' in replies:
    #                     params = self.init_params()
    #                     params["fields"] = self.COMMENTS_FIELDS
    #                     replies = self.get_all_request(comment.get('id') + '/replies', params)
    #                 else:
    #                     replies = replies.get('data')
    #
    #                 # 대댓글 최초 등록순으로
    #                 replies = sorted(replies, key=lambda k: k['timestamp'])
    #                 for reply in replies:
    #                     reply['timestamp'] = date_formatter.datetime_to_formatted_GMT_YYYY_MM_DD_HH_MM_SS(dateutil.parser.parse(reply['timestamp']))
    #                 comment['replies'] = replies
    #             else:
    #                 comment['replies'] = None
    #     except Exception as e:
    #         print(traceback.format_exc())
    #         raise CustomException('인스타그램 댓글을 가져오는데 실패했습니다.')
    #     return comments
    #
    # #
    # # def get_all_media_list(self, instagram_business_account_id):
    # #     '''
    # #     인스타그램 계정의 미디어 전체 리스트 가져오기
    # #     '''
    # #     try:
    # #         params = self.init_params()
    # #         params['fields'] = self.MEDIA_FIELDS
    # #         media = self.get_all_request(instagram_business_account_id + '/media', params)
    # #     except Exception as e:
    # #         raise CustomException('인스타그램 미디어를 가져오는데 실패했습니다.')
    # #
    # #     return media
    #
    # def get_media_detail(self, media_id, is_save_able=True):
    #     '''
    #     미디어의 상제 정보 가져오기
    #     '''
    #     try:
    #         params = self.init_params()
    #         params['fields'] = self.MEDIA_FIELDS
    #         media = self.graph.request(media_id, args=params)
    #         # print("get_media_detail")
    #         media['timestamp'] = date_formatter.datetime_to_formatted_GMT_YYYY_MM_DD_HH_MM_SS(dateutil.parser.parse(media['timestamp']))
    #
    #         # 댓글의 댓글 data set
    #         comments = media.get('comments', None)
    #         if comments:
    #             comments = comments.get('data')
    #             for comment in comments:
    #                 if 'replies' in comment:
    #                     replies = comment.get('replies')
    #
    #                     # 대댓글 paging 있으면 전체 가져오기, paging 없으면 detail 호출시 가져온 replies로 처리
    #                     if 'paging' in replies:
    #                         params = self.init_params()
    #                         params["fields"] = self.COMMENTS_FIELDS
    #                         replies = self.get_all_request(comment.get('id') + '/replies', params)
    #                     else:
    #                         replies = replies.get('data')
    #
    #                     # 대댓글 최초 등록순으로
    #                     replies = sorted(replies, key=lambda k: k['timestamp'])
    #                     for reply in replies:
    #                         reply['timestamp'] = date_formatter.datetime_to_formatted_GMT_YYYY_MM_DD_HH_MM_SS(dateutil.parser.parse(reply['timestamp']))
    #                     comment['replies'] = replies
    #                 else:
    #                     comment['replies'] = None
    #
    #             # 댓글 최신순
    #             media['comments']['data'] = sorted(comments, key=lambda k: k['timestamp'], reverse=True)
    #
    #         if is_save_able:
    #             save_data = self.get_media_type_insights(media_id)[media_id]['data']
    #             for data in save_data:
    #                 if data.get('name') == 'saved':
    #                     media['saved'] = data['values'][0]['value']
    #                 if data.get('name') == 'engagement':
    #                     media['engagement'] = data['values'][0]['value']
    #                 if data.get('name') == 'impressions':
    #                     media['impressions'] = data['values'][0]['value']
    #                 if data.get('name') == 'reach':
    #                     media['reach'] = data['values'][0]['value']
    #
    #     except CustomException as ce:
    #         raise CustomException(str(ce))
    #
    #     except Exception as e:
    #         print(e)
    #         raise CustomException('인스타그램 미디어를 가져오는데 실패했습니다.')
    #
    #     return media
    #
    #
    # def get_media_detail_hourly(self, media_id, is_save_able=True):
    #     '''
    #     미디어의 상제 정보 가져오기
    #     '''
    #     try:
    #         params = self.init_params()
    #         params['after'] = None
    #         params['fields'] = self.MEDIA_FIELDS
    #         media = self.graph.request(media_id, args=params)
    #         # print("get_media_detail")
    #         media['timestamp'] = date_formatter.datetime_to_formatted_GMT_YYYY_MM_DD_HH_MM_SS(
    #             dateutil.parser.parse(media['timestamp']))
    #
    #         # 댓글의 댓글 data set
    #         comments = media.get('comments', None)
    #         if comments:
    #             comments = comments.get('data')
    #             for comment in comments:
    #                 if 'replies' in comment:
    #                     replies = comment.get('replies')
    #
    #                     # 대댓글 paging 있으면 전체 가져오기, paging 없으면 detail 호출시 가져온 replies로 처리
    #                     if 'paging' in replies:
    #                         params = self.init_params()
    #                         params["fields"] = self.COMMENTS_FIELDS
    #                         replies = self.get_all_request(comment.get('id') + '/replies', params)
    #                     else:
    #                         replies = replies.get('data')
    #
    #                     # 대댓글 최초 등록순으로
    #                     replies = sorted(replies, key=lambda k: k['timestamp'])
    #                     for reply in replies:
    #                         reply['timestamp'] = date_formatter.datetime_to_formatted_GMT_YYYY_MM_DD_HH_MM_SS(
    #                             dateutil.parser.parse(reply['timestamp']))
    #                     comment['replies'] = replies
    #                 else:
    #                     comment['replies'] = None
    #
    #         if is_save_able:
    #             save_data = self.get_media_type_insights(media_id)[media_id]['data']
    #             for data in save_data:
    #                 if data.get('name') == 'saved':
    #                     media['saved'] = data['values'][0]['value']
    #                 if data.get('name') == 'engagement':
    #                     media['engagement'] = data['values'][0]['value']
    #                 if data.get('name') == 'impressions':
    #                     media['impressions'] = data['values'][0]['value']
    #                 if data.get('name') == 'reach':
    #                     media['reach'] = data['values'][0]['value']
    #
    #     except CustomException as ce:
    #         raise CustomException(str(ce))
    #
    #     except Exception as e:
    #         print(e)
    #         raise CustomException('인스타그램 미디어를 가져오는데 실패했습니다.')
    #
    #     return media
    #
    #
    # def request_comment_post(self, media_id, message):
    #     '''
    #     comment POST
    #     '''
    #     try:
    #         params = self.params
    #         params['message'] = message
    #         res = self.graph.request(media_id + '/comments', post_args=params, method="POST")
    #
    #     except Exception as e:
    #         raise CustomException('댓글 올리기에 실패했습니다.')
    #     return res
    #
    # def get_user_age_gender(self, instagram_business_account_id):
    #     '''
    #     인스타그램 계정의 demographics 가져오기
    #     '''
    #     ig_demographics = {}
    #     try:
    #         params = self.init_params()
    #         params["metric"] = "audience_gender_age"
    #         params["period"] = "lifetime"
    #         ig_demographics = self.graph.request(instagram_business_account_id + "/insights", args=params)['data']
    #
    #         data = {
    #             "F.13-17": 0,
    #             "F.18-24": 0,
    #             "F.25-34": 0,
    #             "F.35-44": 0,
    #             "F.45-54": 0,
    #             "F.55-64": 0,
    #             "F.65+": 0,
    #             "M.13-17": 0,
    #             "M.18-24": 0,
    #             "M.25-34": 0,
    #             "M.35-44": 0,
    #             "M.45-54": 0,
    #             "M.55-64": 0,
    #             "M.65+": 0,
    #             "U.13-17": 0,
    #             "U.18-24": 0,
    #             "U.25-34": 0,
    #             "U.35-44": 0,
    #             "U.45-54": 0,
    #             "U.55-64": 0,
    #             "U.65+": 0
    #         }
    #
    #         if len(ig_demographics) > 0:
    #             demographics = ig_demographics[0]['values'][0]['value']
    #             for d in data:
    #                 data[d] = demographics.get(d, 0)
    #             ig_demographics[0]['values'][0]['value'] = data
    #         else:
    #             ig_demographics = [
    #                 {
    #                     'values': [
    #                         {
    #                             'value': data
    #                         }
    #                     ]
    #                 }
    #             ]
    #     except facebook.GraphAPIError as e:
    #         error = e.result['error']
    #         code = error['code']
    #         message = error['message']
    #         if 'permission' in message:
    #             raise FacebookGraphAPIError('페이스북 페이지 접근 권한이 수정되어 데이터 확인이 불가합니다./n페이스북 비즈니스 관리자에서 회원님의 접근권한을 확인해 주세요./n문의사항은 help@bigcial.com으로 연락 바랍니다.')
    #         else:
    #             raise
    #     except Exception as e:
    #         raise CustomException('인스타그램 계정 정보를 가져오는데 실패했습니다.')
    #     return ig_demographics
    #
    # def get_media_type_insights(self, media_ids, media_type=None):
    #     '''
    #     media의 type 별 insight 가져오기
    #     '''
    #     if len(media_ids) > 0:
    #         # media_type 별 metric 설정
    #         params = {}
    #
    #         if media_type == 'IMAGE':
    #             params['metric'] = self.PHOTO_METRICS
    #         elif media_type == 'VIDEO':
    #             params['metric'] = self.VIDEO_METRICS
    #         elif media_type == 'CAROUSEL_ALBUM':
    #             params['metric'] = self.CAROUSEL_METRICS
    #         elif media_type == 'STORY':
    #             params['metric'] = self.STORY_METRICS
    #         else:
    #             params['metric'] = self.PHOTO_METRICS
    #
    #         # media 별 insights 가져오기
    #         try:
    #             # media_ids 가 str 타입일 때
    #             if type(media_ids) is str:
    #                 params['ids'] = media_ids
    #             # media_ids 가 복수일 때
    #             elif len(media_ids) > 1:
    #                 ids = ','.join(media_ids)
    #                 params['ids'] = ids
    #             # media_ids 가 단수일 때
    #             else:
    #                 params['id'] = ''.join(media_ids)
    #             # print('##### params', params)
    #             media_insight = self.graph.request('/insights', args=params)
    #
    #             if len(media_ids) == 1:
    #                 media_insight = {
    #                     ''.join(media_ids): media_insight
    #                 }
    #                 # print("media_insight : ", media_insight)
    #
    #         except facebook.GraphAPIError as e:
    #             msg = '인스타그램 미디어 타입별 인사이트를 가져오는데 실패했습니다.'
    #             error = e.result['error']
    #             error_subcode = error['error_subcode']
    #             if error_subcode == 2108006:
    #                 msg = '비즈니스 계정 전환 전 업로드된 게시물의 경우 데이터 확인이 불가합니다.'
    #                 raise CustomException(msg)
    #
    #             message = error['message']
    #             if 'permission' in message:
    #                 raise FacebookGraphAPIError('페이스북 페이지 접근 권한이 수정되어 데이터 확인이 불가합니다./n페이스북 비즈니스 관리자에서 회원님의 접근권한을 확인해 주세요./n문의사항은 help@bigcial.com으로 연락 바랍니다.')
    #             else:
    #                 raise
    #
    #         except Exception as e:
    #             print(traceback.format_exc())
    #             raise CustomException('인스타그램 미디어 타입별 인사이트를 가져오는데 실패했습니다.')
    #             # print('인스타그램 미디어 타입별 인사이트를 가져오는데 실패했습니다.')
    #
    #         return media_insight
    #     else:
    #         return None
    #
    # def get_media_type_insights_hourly(self, media_id, media_type=None):
    #     '''
    #     media의 type 별 insight 가져오기
    #     '''
    #     if media_id is not None:
    #         # media_type 별 metric 설정
    #         params = {}
    #         params['after'] = None
    #
    #         if media_type == 'IMAGE':
    #             params['metric'] = self.PHOTO_METRICS
    #         elif media_type == 'VIDEO':
    #             params['metric'] = self.VIDEO_METRICS
    #         elif media_type == 'CAROUSEL_ALBUM':
    #             params['metric'] = self.CAROUSEL_METRICS
    #         elif media_type == 'STORY':
    #             params['metric'] = self.STORY_METRICS
    #         else:
    #             params['metric'] = self.PHOTO_METRICS
    #
    #         # media 별 insights 가져오기
    #         try:
    #             # media_ids 가 str 타입일 때
    #             if type(media_id) is str:
    #                 params['id'] = media_id
    #             else:
    #                 params['id'] = str(media_id)
    #             # print('##### params', params)
    #             media_insight = self.graph.request('/insights', args=params)
    #
    #             media_insight = {
    #                 str(media_id): media_insight
    #             }
    #
    #         except facebook.GraphAPIError as e:
    #             msg = '인스타그램 미디어 타입별 인사이트를 가져오는데 실패했습니다.'
    #             error = e.result['error']
    #             error_subcode = error['error_subcode']
    #             if error_subcode == 2108006:
    #                 msg = '비즈니스 계정 전환 전 업로드된 게시물의 경우 데이터 확인이 불가합니다.'
    #                 raise CustomException(msg)
    #
    #             message = error['message']
    #             if 'permission' in message:
    #                 raise FacebookGraphAPIError('페이스북 페이지 접근 권한이 수정되어 데이터 확인이 불가합니다./n페이스북 비즈니스 관리자에서 회원님의 접근권한을 확인해 주세요./n문의사항은 help@bigcial.com으로 연락 바랍니다.')
    #             else:
    #                 raise
    #
    #         except Exception as e:
    #             print(traceback.format_exc())
    #             raise CustomException('인스타그램 미디어 타입별 인사이트를 가져오는데 실패했습니다.')
    #             # print('인스타그램 미디어 타입별 인사이트를 가져오는데 실패했습니다.')
    #
    #         return media_insight
    #     else:
    #         return None
    #
    # def get_media_insight(self, media_id, metric=PHOTO_METRICS):
    #     '''
    #     인스타그램 미디어 인사이트 가져오기
    #     '''
    #     try:
    #         params = {}
    #         params['metric'] = metric
    #         media_insight = self.graph.request(media_id + '/insights', args=params)
    #     except Exception as e:
    #         return None
    #         # raise CustomException('인스타그램 미디어 타입별 인사이트를 가져오는데 실패했습니다.')
    #
    #     return media_insight
    #
    # def get_followers_insights(self, instagram_business_account_id, since=None, until=None):
    #     '''
    #     인스타그램 계정의 팔로워 추이 가져오기
    #     '''
    #     params = self.init_params()
    #     params['metric'] = self.FOLLOWERS_INSIGHTS_METRICS
    #     params['period'] = 'day'
    #
    #     if until is None:
    #         until = datetime.now() - timedelta(days=1)
    #
    #     if since is None:
    #         since = until - timedelta(days=30)
    #
    #     since_timestamp = int(time.mktime(since.timetuple()))
    #     until_timestamp = int(time.mktime(until.timetuple()))
    #     params['since'] = since_timestamp
    #     params['until'] = until_timestamp
    #
    #     insights = self.graph.request(instagram_business_account_id + '/insights', args=params)['data']
    #     followers_insights = []
    #     for insight in insights:
    #         if insight['name'] == 'follower_count':
    #             followers_insights = insight['values']
    #
    #     return followers_insights
    #
    # def get_online_followers(self, instagram_business_account_id, since, until):
    #     '''
    #     인스타그램 계정의 활성 팔로워 정보 가져오기
    #     '''
    #     weekday = [
    #         'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'
    #     ]
    #     hours = {
    #         '0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0,
    #         '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0, '23': 0
    #     }
    #     online_followers = [
    #         {weekday[0]: copy.deepcopy(hours)}, {weekday[1]: copy.deepcopy(hours)}, {weekday[2]: copy.deepcopy(hours)},
    #         {weekday[3]: copy.deepcopy(hours)}, {weekday[4]: copy.deepcopy(hours)}, {weekday[5]: copy.deepcopy(hours)},
    #         {weekday[6]: copy.deepcopy(hours)}
    #     ]
    #
    #     try:
    #         params = self.init_params()
    #         params['metric'] = self.ONLINE_FOLLOWERS_METRICS
    #         params['period'] = 'lifetime'
    #
    #         if since is None:
    #             since_datetime = datetime.now() - timedelta(days=28)
    #         else:
    #             since_datetime = datetime.strptime(since, '%Y%m%d')
    #
    #         if until is None:
    #             until_datetime = datetime.now()
    #         else:
    #             until_datetime = datetime.strptime(until, '%Y%m%d') + timedelta(days=1)
    #
    #         since_timestamp = time.mktime(since_datetime.timetuple())
    #         until_timestamp = time.mktime(until_datetime.timetuple())
    #         params['since'] = since_timestamp
    #         params['until'] = until_timestamp
    #
    #         values = self.graph.request(instagram_business_account_id + '/insights', args=params)['data'][0]['values']
    #         for item in values:
    #             weekday_index = datetime.strptime(item['end_time'], '%Y-%m-%dT%H:%M:%S+0000').weekday()
    #             value = item['value']
    #             for key, value in value.items():
    #                 online_followers[weekday_index][weekday[weekday_index]][key] += value
    #         return online_followers
    #     except Exception as e:
    #         print(traceback.format_exc())
    #
    # def get_profile_views(self, instagram_business_account_id, since, until):
    #     '''
    #     인스타그램 계정의 impressions, reach, profile_views 가져오기
    #     '''
    #     try:
    #         params = self.init_params()
    #         params['metric'] = 'impressions,reach,profile_views'
    #         params['period'] = 'day'
    #
    #         since_timestamp = time.mktime(datetime.strptime(since, '%Y%m%d').timetuple())
    #         until_timestamp = time.mktime((datetime.strptime(until, '%Y%m%d') + timedelta(days=1)).timetuple())
    #
    #         ig_profile_views = []
    #         between_days = (datetime.fromtimestamp(until_timestamp) - datetime.fromtimestamp(since_timestamp)).days
    #
    #         if between_days > 30:
    #             month_timestamp = 60 * 60 * 24 * 30
    #             call_count = int(math.ceil(between_days / 30))
    #             for call in range(call_count):
    #                 params['since'] = datetime.fromtimestamp(until_timestamp - (month_timestamp * (call + 1)))
    #                 params['until'] = until_timestamp - (month_timestamp * call)
    #                 insights = self.graph.request(instagram_business_account_id + '/insights', args=params)['data']
    #
    #                 # 첫번째 호출
    #                 if call == 0:
    #                     ig_profile_views.extend(insights)
    #                 else:
    #                     for index, insight in enumerate(insights):
    #                         # 마지막 호출
    #                         if call == (call_count - 1):
    #                             remainder = between_days % (30 * call)
    #                             ig_profile_views[index]['values'].extend(insight['values'][::-1][:remainder])
    #                         else:
    #                             ig_profile_views[index]['values'].extend(insight['values'])
    #             # 날짜순 정렬
    #             for ig_profile_view in ig_profile_views:
    #                 ig_profile_view['values'] = sorted(ig_profile_view['values'], key=itemgetter('end_time'))
    #         else:
    #             params['since'] = since_timestamp
    #             params['until'] = until_timestamp
    #             ig_profile_views.extend(
    #                 self.graph.request(instagram_business_account_id + '/insights', args=params)['data'])
    #         return ig_profile_views
    #     except facebook.GraphAPIError as e:
    #         error = e.result['error']
    #         code = error['code']
    #         message = error['message']
    #         if 'permission' in message:
    #             raise FacebookGraphAPIError('페이스북 페이지 접근 권한이 수정되어 데이터 확인이 불가합니다./n페이스북 비즈니스 관리자에서 회원님의 접근권한을 확인해 주세요./n문의사항은 help@bigcial.com으로 연락 바랍니다.')
    #         else:
    #             raise
    #     except Exception as e:
    #         raise
    #
    # def get_tagged_media_list(self, instagram_business_account_id, after=None):
    #     '''
    #     인스타그램 비즈니스 계정이 태그된 미디어 가져오기
    #     '''
    #
    #     params = self.init_params()
    #     params['fields'] = self.TAGS_FIELDS
    #     if after:
    #         params['after'] = after
    #     ig_tagged_medias = self.graph.request(instagram_business_account_id + '/tags', args=params)
    #     return ig_tagged_medias
    #
    # def get_mentioned_media(self, instagram_business_account_id, media_id):
    #     try:
    #         params = {}
    #         params['fields'] = "mentioned_media.media_id(" + str(media_id) + "){" + self.MENTIONED_MEDIA_FIELDS + "}"
    #         # print(params)
    #
    #         res = self.graph.request(instagram_business_account_id + '/', args=params)
    #
    #     except Exception as e:
    #         # print(traceback.format_exc())
    #         # raise CustomException('댓글 올리기에 실패했습니다.')
    #         # print("PASS")
    #         res = None
    #     return res
    #
    # def get_mentioned_comment(self, instagram_business_account_id, comment_id):
    #     try:
    #         params = {}
    #         params['fields'] = "mentioned_comment.comment_id(" + str(
    #             comment_id) + "){" + self.MENTIONED_COMMENT_FIELDS + "}"
    #         # print(params)
    #
    #         res = self.graph.request(instagram_business_account_id + '/', args=params)
    #
    #     except Exception as e:
    #         # print(traceback.format_exc())
    #         # raise CustomException('댓글 올리기에 실패했습니다.')
    #         # print("PASS")
    #         res = None
    #     return res
    #
    # def get_business_insight_lifetime(self, instagram_business_account_id, since=None, until=None, field=INSTAGRAM_BUSINESS_ACCOUNT_INSIGHT_LIFETIME):
    #     insights = None
    #     try:
    #
    #         if since is None or until is None:
    #             # online_followers은 기본이 이틀전
    #             if 'online_followers' == field:
    #                 since = datetime.strftime(date.today() - timedelta(4), '%Y%m%d')
    #                 until = datetime.strftime(date.today() - timedelta(2), '%Y%m%d')
    #             else:
    #                 since = datetime.strftime(date.today() - timedelta(1), '%Y%m%d')
    #                 until = datetime.strftime(date.today(), '%Y%m%d')
    #
    #
    #         # 20200114
    #         since = date_formatter.str_to_datetime(since, '%Y%m%d')
    #         until = date_formatter.str_to_datetime(until, '%Y%m%d')
    #         since_timestamp = int(time.mktime(since.timetuple()))
    #         until_timestamp = int(time.mktime(until.timetuple()))
    #
    #         params = {
    #             "metric": field,
    #             "period": "lifetime",
    #             "since": since_timestamp,
    #             "until": until_timestamp
    #         }
    #
    #         insights = self.graph.request(str(instagram_business_account_id) + "/insights", args=params)
    #
    #     except Exception as e:
    #         print(traceback.format_exc())
    #         # raise e
    #     return insights
    #
    # def get_business_insight_day(self, instagram_business_account_id, since=None, until=None):
    #     insights = None
    #     try:
    #
    #         if since is None or until is None:
    #             since = datetime.strftime(date.today() - timedelta(1), '%Y%m%d')
    #             until = datetime.strftime(date.today(), '%Y%m%d')
    #
    #         # 20200114
    #         since = date_formatter.str_to_datetime(since, '%Y%m%d')
    #         until = date_formatter.str_to_datetime(until, '%Y%m%d')
    #         since_timestamp = int(time.mktime(since.timetuple()))
    #         until_timestamp = int(time.mktime(until.timetuple()))
    #
    #         params = {
    #             "metric": self.INSTAGRAM_BUSINESS_ACCOUNT_INSIGHT_DAY,
    #             "period": "day",
    #             "since": since_timestamp,
    #             "until": until_timestamp
    #         }
    #
    #         insights = self.graph.request(str(instagram_business_account_id) + "/insights", args=params)
    #
    #     except Exception as e:
    #         print(traceback.format_exc())
    #         # raise e
    #     return insights
    #
    # def get_online_followers(self, instagram_business_account_id, since, until):
    #     insights = None
    #     try:
    #         params = {
    #             'metric': 'online_followers',
    #             'period': 'lifetime',
    #             'since': since,
    #             'until': until
    #         }
    #         insights = self.graph.request(str(instagram_business_account_id) + "/insights", args=params)
    #     except facebook.GraphAPIError as e:
    #         error = e.result['error']
    #         code = error['code']
    #         message = error['message']
    #         if 'permission' in message:
    #             raise FacebookGraphAPIError('페이스북 페이지 접근 권한이 수정되어 데이터 확인이 불가합니다./n페이스북 비즈니스 관리자에서 회원님의 접근권한을 확인해 주세요./n문의사항은 help@bigcial.com으로 연락 바랍니다.')
    #         else:
    #             raise
    #     except Exception as e:
    #         print(traceback.format_exc())
    #     return insights
    #
    # def get_app_permissions(self):
    #     try:
    #         params = {}
    #         permissions = self.get_all_request("me/permissions", params)
    #     except Exception as e:
    #         print(traceback.format_exc())
    #         logger.error(traceback.format_exc())
    #     return permissions
    #
    # def get_hashtag_id(self, instagram_business_account_id, hashtag_name):
    #     try:
    #         params = {
    #             'user_id': instagram_business_account_id,
    #             'q': hashtag_name
    #         }
    #         result = self.graph.request("ig_hashtag_search", params)
    #         hashtag_id = result.get('data')[0].get('id')
    #     except Exception as e:
    #         print(traceback.format_exc())
    #     return hashtag_id
    #
    # def get_hashtag_recent_media(self, instagram_business_account_id, hashtag_id, after=None):
    #     try:
    #         data = {}
    #         medias = []
    #         params = {
    #             'user_id': instagram_business_account_id,
    #             'fields': 'like_count,media_type,permalink',
    #         }
    #         if after:
    #             params['after'] = after
    #         result = self.graph.request(str(hashtag_id) + '/recent_media', params)
    #         data['medias'] = result.get('data')
    #
    #         paging = result.get('paging', None)
    #         data['after'] = None
    #         if paging:
    #             cursors = paging.get('cursors', None)
    #             if cursors:
    #                 data['after'] = cursors.get('after', None)
    #     except Exception as e:
    #         print(traceback.format_exc())
    #     return data
    #
    # def get_hashtag_top_media(self, instagram_business_account_id, hashtag_id):
    #     try:
    #         medias = []
    #         params = {
    #             'user_id': instagram_business_account_id,
    #             'fields': 'like_count,media_type,permalink',
    #             'limit': 9
    #         }
    #         result = self.graph.request(str(hashtag_id) + '/top_media', params)
    #         medias = result.get('data')
    #     except Exception as e:
    #         print(traceback.format_exc())
    #     return medias