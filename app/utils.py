import datetime
import operator
from flask.ext.login import current_user
from core import db
from sqlalchemy import desc
from sqlalchemy.exc import InvalidRequestError, IntegrityError


def get_items(model, request):
    ops = {
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge,
        '==': operator.eq,
        '!=': operator.ne
    }

    sort = request.args.get('sort')
    limit = request.args.get('limit')
    filters = request.args.get('filter').split(',') if\
        request.args.get('filter') else []
    desc_order = False

    response = {'errors': []}
    order_param = None
    limit_param = None
    filters_param = []

    if sort and sort[0] == '-':
        desc_order = True
        sort = sort[1:]

    if sort and sort not in model.sortable():
        response['errors'].append('Invalid sort parameter.')
    elif sort:
        order_param = desc(getattr(model, sort)) if desc_order\
            else getattr(model, sort)

    if limit and not is_int(limit):
        response['errors'].append('Invalid limit parameter.')
    elif limit:
        limit_param = int(limit)

    for s in filters:
        try:
            opr = ops[OPS_REGEX.search(s).group(0)]
        except AttributeError:
            response['errors'].append('Invalid filter parameter.')
            break

        toks = OPS_REGEX.split(s)
        if len(toks) != 2 or toks[0] not in model.sortable():
            response['errors'].append('Invalid filter parameter.')
            break

        attr = getattr(model, toks[0])
        if toks[0] == 'date' and not is_number(toks[1]):
            response['errors'].append('Invalid filter parameter.')
            break
        elif toks[0] == 'date':
            value = datetime.datetime.fromtimestamp(float(toks[1]))
        else:
            value = float(toks[1]) if is_number(toks[1]) else toks[1]

        filters_param.append(opr(attr, value))

    if not response['errors']:
        try:
            response['payload'] = [i.serialize for i in
                                   db.session.query(model)
                                   .filter(*filters_param)
                                   .filter_by(user=current_user)
                                   .order_by(order_param).limit(limit_param)]
        except InvalidRequestError:
            response['errors'].append('Invalid filter parameter.')

    response['success'] = not response['errors']
    return response


def get_item(item_id, model, user=None):
    response = {'errors': []}
    item = db.session.query(model).get(item_id)

    if not item:
        response['errors'].append('Does not exist.')
    elif user and item.user != current_user:
        response['errors'].append('Forbidden.')
    else:
        response['payload'] = item.serialize
    response['success'] = not response['errors']
    return response


def get_or_create(json, model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()

    if instance:
        return instance
    else:
        instance = model(json)
        db.session.add(instance)
        db.session.commit()
        return instance
