from flask import jsonify, request, current_app
from datetime import date
from ..policy import Policy
from ..models import Activity, ActivityType
from ..utils import get_policy_class, get_all_stages, get_activity_class
from . import bp


@bp.route('/<string:lang>/<string:stage>/policy/<string:policy_number>/<string:effective_date>')
@bp.route('/<string:lang>/<string:stage>/policy/<string:policy_number>')
def get_policy(lang, stage, policy_number, effective_date=None):
    #
    # fetches a Policy by policy_number & effective_data
    # and returns it
    #

    # set default effective_date if needed
    if effective_date is None:
        effective_date = str(date.today())

    try:
        # get Policy
        policy = get_policy_class()(policy_number, effective_date)
        policy.setStage(stage)
        policy.setLanguage(lang)
        current_app.logger.warning(f"Stage={stage}, lang={lang}")

        if policy.fetch():
            current_app.config['POLICIES'][policy.uuid] = policy
            result = policy.get()
            # DEBUG
            #import json 
            #print(json.dumps(result, indent=2))
            
            # set response
            response_code = 400 if 'error' in result else 200
            return jsonify(result), response_code


    except Exception as e:
        current_app.logger.exception(f'Fetch policy {policy_number} {effective_date} failed: {e}')
        return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'Policy not found'}), 404


@bp.route('/stage')
def get_stages():
    #
    # returns list of all available stages
    #

    try:
        # get all stages
        stages = get_all_stages()()
        current_app.logger.debug(f"Value of stages: {stages}")
    except Exception as e:
        current_app.logger.warning(f'Failed to get All Stages: {e}')
        stages = []

    return jsonify(stages), 200


@bp.route(f'/<string:lang>/<string:stage>/activity', methods=['POST'])
def new_activity(lang, stage):
    #
    # create new activity
    #

    # get post data
    data = request.get_json()

    # get policy and create activity 
    try:
        # get policy from app store
        policy = current_app.config['POLICIES'].get(data['id'])
        if policy is None:
            raise Exception(f'Policy {data["id"]} is absent in PoLZy storage')

        # save activity to DB
        activity = Activity.new(data, policy)

        # execute activity
        if policy.executeActivity(data['activity']):

            # update activity
            activity.finish()
            # update policy
            current_app.logger.warning(f"Stage={stage}, lang={lang}")
            policy.setStage(stage)
            policy.setLanguage(lang)
            policy.fetch()
            if data['activity'] == "Detailauskunft":
                print(f"returned link: {policy.returnLink()}")
                return jsonify({"link": policy.returnLink()}), 200
            else:
                print(f"Activity was: {data['activity']}")

            return jsonify(policy.get()), 200
        
    except Exception as e:
        current_app.logger.warning(f'Execution activity {data.get("name")} for policy {policy.policy_number} faild: {e}')
        return jsonify({'error': 'Bad Request'}), 400

    return jsonify({
        'id': str(activity.id),
        'status': 'accepted',
        'msg': 'Activity accepted',
    }), 202
