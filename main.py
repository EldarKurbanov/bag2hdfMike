import bagpy
import pandas
import h5py

if __name__ == '__main__':
    hdfFile = h5py.File("reinforcement_ros_data.hdf5", "w")

    bagreader = bagpy.bagreader('klyachin.bag')
    laserScanCSV = bagreader.message_by_topic('/diffbot/scan')
    twistCSV = bagreader.message_by_topic('/diffbot/mobile_base_controller/cmd_vel')
    rewardCSV = bagreader.message_by_topic('/reward_node')

    laserScan = pandas.read_csv(laserScanCSV)
    twist = pandas.read_csv(twistCSV)
    reward = pandas.read_csv(rewardCSV)

    firstStepTime = 0
    currentStep = 0
    count = 0

    for i, currentTwist in twist.iterrows():
        if currentStep == 0 and \
                (currentTwist['linear.x'] != 0 or currentTwist['linear.y'] != 0 or currentTwist['linear.z'] != 0 or
                 currentTwist['angular.x'] != 0 or currentTwist['angular.y'] != 0 or currentTwist['angular.z'] != 0):
            currentStep = 1
            firstStepTime = currentTwist['Time']
            hdfFile["laserScan"][0][i] = "sdfisdfjo"
            # record twist
            continue
        if currentStep == 1:
            currentTime = currentTwist['Time']
            if firstStepTime + 0.5 < currentTime:
                currentStep = 2
            continue
        if currentStep == 2:
            # record reward
            currentStep = 0
            count += 1

    hdfFile.close()
    print(count)
