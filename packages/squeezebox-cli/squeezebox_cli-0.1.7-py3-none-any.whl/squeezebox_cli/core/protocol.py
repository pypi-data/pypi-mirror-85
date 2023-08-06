from urllib.parse import quote, unquote


def send_receive(tn, fields):
    tn.write(' '.join(map(quote, fields)).encode('utf-8') + b'\n')
    return receive(tn)


def receive(tn):
    return list(map(
        lambda f: unquote(f).rstrip(),
        tn.read_until(b'\n').decode('utf-8').split(' ')))


def tagged_command(args, tags):
    return list(map(str, args)) + list(map(':'.join, tags))


def parse_tags(fields):
    # print(f'parse_tags: {fields}')
    tags = []
    for f in fields:
        try:
            k, v = f.split(':', 1)
            tags.append((k, v))
        except ValueError:
            # ignore field if not a key-value pair
            pass
    return tags


def chunked_query(tn, command, chunk_size, group_tag, args=[]):
    count = None
    tag_groups = []
    start = 0
    group_count = 0
    while count is None or len(tag_groups) < count:
        # print(count, len(tag_groups))
        for k, v in parse_tags(
                send_receive(
                    tn,
                    [command, f'{start}', f'{chunk_size}'] + args)
                )[len(args):]:
            if k == 'count':
                count = int(v)
            elif k == group_tag:
                tag_groups.append([(k, v)])
            else:
                tag_groups[-1].append((k, v))
        start += chunk_size
        if group_count == len(tag_groups):
            # we're not finding new groups
            # TODO: raise a more specific exception
            print(
                    f'chunked_query({tn}, {command}, {chunk_size},'
                    f' {group_tag}, {args}')
            raise Exception
        group_count = len(tag_groups)
    return tag_groups


def query_to_single_values(
        tn, command, chunk_size, grouping_tag, result_tag, query_tags=[]):
    tag_groups = chunked_query(
            tn, command, chunk_size, grouping_tag, args=query_tags)
    results = dict()
    for tg in tag_groups:
        id = None
        g = None
        for k, v in tg:
            if k == 'id':
                id = int(v)
            elif k == result_tag:
                g = v
        results[id] = g
    return results


def query_to_dicts(
        tn, command, chunk_size, grouping_tag, args, tag_handlers,
        strict=False):
    tag_groups = chunked_query(
            tn, command, chunk_size, grouping_tag, args=args)
    results = []
    for tg in tag_groups:
        group = dict()
        for k, v in tg:
            try:
                group[k] = tag_handlers[k](v)
            except KeyError:
                if not strict:
                    group[k] = str(v)
        results.append(group)
    return results
