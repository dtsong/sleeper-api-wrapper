# Drafts
`sleeper_wrapper.Drafts(draft_id)`

Instantiating a `Drafts` object will allow interaction with Sleeper's [Drafts endpoint](https://docs.sleeper.com/#drafts) by pulling data for the draft specified by the `draft_id`. Examples for how the data is structured for methods hitting the API directly may be found in their documentation for the endpoint.

## Attributes
`draft_id` _(Union[int, str])_: The Sleeper ID for the draft. May be provided as a string or int.

## Methods
`get_specific_draft`(): Returns the draft's data, such as draft settings, start time, league information, and order. It does not include the picks themselves.

`get_all_picks`(): Returns all the picks in the specified draft.

`get_traded_picks`(): Returns all the traded picks in the specified draft.

## Examples
```
from sleeper_wrapper import Drafts

drafts = Drafts(draft_id="992218427449999361")
my_draft = drafts.get_specific_draft()
all_picks = drafts.get_all_picks()
```
