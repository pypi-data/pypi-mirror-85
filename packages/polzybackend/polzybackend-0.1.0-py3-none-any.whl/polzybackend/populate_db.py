#
# populates PoLZy db with sample instances
#

from . import db
from .models import User, ActivityType, OAuthProvider
from .auth import generate_token
from .policy import Policy
import uuid
from datetime import datetime, timedelta


# create OAuth provider
print('Creating OAuth Provider...')
provider = OAuthProvider(
    name='SampleProvider',
    client_id=str(uuid.uuid4()),
    secret_key=generate_token(16),
)
db.session.add(provider)

# create users
print('Creating users...')
user = User(
    email='admin@sample.com',
    oauth_provider=provider,
    oauth_user_id=str(uuid.uuid4()),
    oauth_token=generate_token(16),
    key_expired=datetime.now() + timedelta(days=360),
)
db.session.add(user)

# create activity types
print('Creating Activity Types...')
activities = {}
for name in {i for key, value in Policy.activities_by_status.items() for i in value}:
    activity = ActivityType(
        name=name,
        description=f'Sample {name.capitalize()} Activity',
    )
    db.session.add(activity)

# save to db
db.session.commit()
print('Done.')
