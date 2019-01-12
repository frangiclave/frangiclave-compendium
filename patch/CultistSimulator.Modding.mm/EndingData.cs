using System;
using Assets.Core.Entities;

namespace CultistSimulator.Modding.mm
{
    [Serializable]
    public class EndingData
    {
        public EndingData(Ending ending)
        {
            id = ending.Id;
            title = ending.Title;
            description = ending.Description;
            imageId = ending.ImageId;
            endingFlavour = ending.EndingFlavour.ToString();
            anim = ending.Anim;
            achievementId = ending.AchievementId;
        }

        public string id;

        public string title;

        public string description;

        public string imageId;

        public string endingFlavour;

        public string anim;

        public string achievementId;
    }
}
