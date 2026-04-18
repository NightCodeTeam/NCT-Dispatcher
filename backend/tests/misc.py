import requests


requests.post(
    'http://localhost:8001/v1/incidents/new',
    json={
        "incident": {
            "title": "Go big or go exist",
            "message": """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut dapibus non orci sed faucibus. Morbi interdum est eu dolor semper mollis. Suspendisse facilisis, neque eget sollicitudin maximus, elit enim auctor neque, vitae commodo elit nisl eu dolor. Proin lacinia porttitor tortor, vitae aliquam neque maximus vitae. Aenean blandit convallis ligula et eleifend. Nullam ornare congue interdum. Donec suscipit tortor quis nisl ultrices ullamcorper. Suspendisse a lacus cursus, facilisis est ac, lacinia arcu. Ut ornare pretium lorem nec vehicula. Donec pharetra risus facilisis quam vulputate, vel volutpat velit venenatis. Nunc in molestie elit.

            Vivamus imperdiet vitae nunc vel gravida. Etiam a urna est. Maecenas viverra eros eu eros mollis, mollis tincidunt dolor lacinia. In hac habitasse platea dictumst. Aenean vel erat non sapien porta posuere. Nulla nec metus velit. Donec vitae iaculis nibh. Proin nibh lacus, tincidunt at tortor eu, sodales ultricies sapien. In at maximus arcu. Quisque laoreet dignissim purus eget vehicula. Curabitur ornare viverra maximus.

            Nulla commodo enim id eros efficitur, id suscipit nisl varius. Aenean condimentum viverra ex id dignissim. Sed laoreet dictum nibh. Quisque fermentum eu arcu eu convallis. Maecenas pretium sollicitudin arcu nec ornare. Mauris placerat lorem nulla, vitae aliquet justo blandit tincidunt. Nunc molestie, neque id tempor sollicitudin, metus justo finibus dolor, a lacinia odio metus sit amet augue. In hac habitasse platea dictumst. Mauris at dapibus ante.

            Morbi euismod risus et tortor euismod, at fermentum tellus interdum. Sed placerat eros ipsum, ac faucibus justo ultricies vitae. Ut et imperdiet justo. Mauris eget congue odio. Duis at tortor cursus, luctus lacus quis, mollis est. Etiam mauris justo, ullamcorper sit amet ex nec, varius tempus ex. Morbi faucibus finibus maximus. Vestibulum dignissim, quam vel viverra commodo, erat elit aliquet tellus, in faucibus justo nisl vitae justo. Suspendisse porta velit in accumsan maximus. Curabitur efficitur sodales leo, sed ultricies risus vulputate sit amet. Praesent venenatis leo eget arcu aliquam finibus. Donec a blandit urna, ut tristique urna. Vivamus vitae nisi eleifend augue viverra iaculis. In hac habitasse platea dictumst. Ut vel nibh consequat, vestibulum purus ac, pulvinar risus. Nunc tempus, lacus eu rhoncus pharetra, risus turpis eleifend est, eu semper elit erat id metus.

            Cras efficitur risus sit amet cursus ultrices. Mauris vestibulum nisi justo. Suspendisse potenti. Morbi nec malesuada lectus. Fusce mollis, diam ac tempor gravida, diam eros aliquam ipsum, a gravida urna ex a ipsum. Aliquam tristique massa ac placerat auctor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aliquam maximus nulla eget feugiat pretium.""",
            "logs": "",
            "level": "error"
        },
        "app_name": "Auth",
        "app_code": "d1BFuVHjRMvjjl0SDUaL"
    }
)
