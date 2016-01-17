import datetime
import operator
from core import db
from exceptions import NotFoundError
from sqlalchemy import desc
from sqlalchemy.exc import InvalidRequestError, IntegrityError


def get_items(model, request, user=None):
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

    errors = []
    order_param = None
    limit_param = None
    filters_param = []

    if sort and sort[0] == '-':
        desc_order = True
        sort = sort[1:]

    if sort and sort not in model.sortable():
        errors.append('Invalid sort parameter.')
    elif sort:
        order_param = desc(getattr(model, sort)) if desc_order\
            else getattr(model, sort)

    if limit and not is_int(limit):
        errors.append('Invalid limit parameter.')
    elif limit:
        limit_param = int(limit)

    for s in filters:
        try:
            opr = ops[OPS_REGEX.search(s).group(0)]
        except AttributeError:
            errors.append('Invalid filter parameter.')
            break

        toks = OPS_REGEX.split(s)
        if len(toks) != 2 or toks[0] not in model.sortable():
            errors.append('Invalid filter parameter.')
            break

        attr = getattr(model, toks[0])
        if toks[0] == 'date' and not is_number(toks[1]):
            errors.append('Invalid filter parameter.')
            break
        elif toks[0] == 'date':
            value = datetime.datetime.fromtimestamp(float(toks[1]))
        else:
            value = float(toks[1]) if is_number(toks[1]) else toks[1]

        filters_param.append(opr(attr, value))

    if not errors:
        try:
            payload = db.session.query(model)\
                .filter(*filters_param)\
                .order_by(order_param)\
                .limit(limit_param)
        except InvalidRequestError:
            errors.append('Invalid filter parameter.')

    if user and not errors:
        payload = payload.filter_by(user=user)

    return {
        'success': not errors,
        'errors': errors,
        'payload': [i.serialize for i in payload]
    }


def get_item(item_id, model, user=None):
    item = db.session.query(model).get(item_id)

    if item is None:
        raise NotFoundError(model)

    if user and item.user != user:
        return {'success': False, 'errors': ['Forbidden.']}
    else:
        return {'success': True, 'payload': item.serialize}


def get_or_create(json, model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()

    if instance:
        return instance
    else:
        instance = model(json)
        db.session.add(instance)
        db.session.commit()
        return instance


# Convert a datetime object to unix epoch
# If no argument is specified gives the current epoch time
def unix_time(dt=datetime.datetime.now()):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()
