from pydantic import BaseModel, Field
from typing import Optional, Literal


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


class EventExtraction(BaseModel):
    """For First LLM call: Extract basic event information"""

    description: str = Field(description="Raw description of the event")
    is_calender_event: bool = Field(description="Wheter this event is a calendar event")
    confidence_score: float = Field(description="Confidence score between 0 and 1")


class EventDetails(BaseModel):
    """For Second LLM call: Parse specific event details"""

    name: str = Field(description="Name of event")
    date: str = Field(
        description="Date and time of the event. Use ISO 8601 to format this value."
    )
    duration_time: int = Field(description="Expected duration in minutes")
    participants: list[str] = Field(description="List of participants")


class EventConfirmation(BaseModel):
    """For Third LLM call"""

    confirmation_message: str = Field(
        description="Natural language confirmation message"
    )
    calendar_link: Optional[str] = Field(
        description="Generated calendar link if applicable"
    )


# define model
class CalendarRequestType(BaseModel):
    """Router LLM call: Determine the type of calendar request"""

    request_type: Literal["new_event", "modify_event", "other"] = Field(
        description="Type of calendar request being made"
    )
    confidence_score: float = Field(description="Confidence score between 0 and 1")
    description: str = Field(description="Cleaned description of the request")


class NewEventDetails(BaseModel):
    """Details for creating a new event"""

    name: str = Field(description="Name of event")
    date: str = Field(description="Date and Time of the event (ISO 8601)")
    duration_minutes: int = Field(description="Duration in minutes")
    participants: list[str] = Field(description="List of participants")


class Change(BaseModel):
    """Details for changing an existing event"""

    field: str = Field(description="Field to change")
    new_value: str = Field(description="New value for the field")


class ModifyEventDetails(BaseModel):
    """Details for modifying an existing event"""

    event_identifier: str = Field(
        description="Description to identify the existing event"
    )
    changes: list[Change] = Field(description="List of changes to make")
    participants_to_add: list[str] = Field(description="New participants to add")
    participants_to_remove: list[str] = Field(description="Participants to remove")


class CalendarResponse(BaseModel):
    """Final Response format"""

    sucess: bool = Field(description="whether the operation was successful")
    message: str = Field(description="User friendly response message")
    calendar_link: Optional[str] = Field(description="Calendar link if applicable")
